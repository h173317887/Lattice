# 从 ZCode 连接 Figma 失败，理解 MCP、进程启动与 PATH

## 先看一个让我产生疑问的例子

我想让 ZCode 读取 Figma 设计稿。一开始按官方远程 MCP 的方式填写：

```text
类型：HTTP
地址：https://mcp.figma.com/mcp
```

结果报错：

```text
Dynamic Client Registration rejected (HTTP 403): Forbidden
```

改用第三方 `figma-developer-mcp`，选择 `stdio`，又遇到：

```text
spawn ENOTDIR
```

后来，我升级了 Node.js，并同时给 `command` 配置绝对路径、给环境变量配置 `PATH`，连接成功了。

这让我产生了几个真正需要弄懂的问题：

> 为什么同样是连接 Figma，一个填 URL，另一个却要执行 `npx`？
>
> `figma-developer-mcp` 到底是一个库、一个服务，还是一个 Node.js 进程？
>
> 既然 `command` 已经写了 `npx` 的完整路径，为什么还要配 `PATH`？
>
> `PATH` 中有好几个目录，系统究竟怎么找？

这些问题看起来分散，但其实可以沿着**一次工具调用是怎么发生的**串起来。

---

## 先搞清楚：我究竟在连接谁

当我向 ZCode 输入：

```text
读取这个 Figma Frame，并生成 Vue 页面。
```

ZCode 中的大模型并不会天然拥有读取 Figma 文件的能力。它需要一个外部程序，提供“读取设计稿”之类的工具。

可以把整个流程拆成两段：

```text
ZCode（MCP Client）
    │
    │ 第一段：调用 MCP 工具
    ▼
figma-developer-mcp（MCP Server）
    │
    │ 第二段：携带 Figma Token，请求 Figma REST API
    ▼
Figma
    │
    │ 返回设计数据
    ▼
figma-developer-mcp 整理结果
    │
    ▼
ZCode 把结果交给模型，模型再生成代码
```

这里最容易混淆的是两个协议边界：

- **ZCode ↔ MCP Server**：双方用 MCP 协议交换工具调用与结果。
- **MCP Server ↔ Figma**：第三方程序通过 Figma REST API 请求数据。

所以，`figma-developer-mcp` 本质上是一个运行在 Node.js 中的 **MCP Server 程序**。它自己不负责大模型推理，主要负责把“读取 Figma”包装成 ZCode 能调用的工具。

也因此，第三方 MCP 能用 `stdio` 连接，并不代表 Figma 官方服务器支持 `stdio`。**它们根本不是同一个服务端。**

---

## 为什么有的 MCP 填 URL，有的却要填 `npx`

起初我容易把 MCP Server 想成传统后端：既然叫 Server，是不是必须启动一个 HTTP 服务、监听端口？

其实不是。“Server”描述的是**提供工具的一方**，不强制规定它和 Client 之间用什么传输方式。

### 第一种：`stdio`——客户端启动一个本地子进程

例如：

```json
{
  "command": "npx",
  "args": ["-y", "figma-developer-mcp", "--stdio"]
}
```

它表达的不是“访问一个网址”，而是：

```text
ZCode
  │
  │ 启动命令 npx ...
  ▼
一个本地 Node.js 子进程
  │
  ├── stdin：接收 ZCode 发来的协议消息
  └── stdout：向 ZCode 返回协议消息
```

`stdin` 是标准输入，`stdout` 是标准输出。MCP 消息通过这两条通道传递，不需要给 MCP 本身额外开一个 HTTP 端口。

**这不意味着程序不能联网。** 它仍然可以在内部通过 HTTPS 请求 Figma。只是 ZCode 与它通信的这一段走的是 stdio。

我可以把 stdio 想成：**ZCode 自己叫来一个帮手，直接通过进程的输入输出和它说话。**

### 第二种：HTTP——服务已经运行，客户端去找它

Figma 官方远程 MCP 的形式是：

```text
ZCode ── HTTP ──> https://mcp.figma.com/mcp
```

这里不需要 ZCode 使用 `npx` 启动 Figma 官方服务器，因为服务器已经由 Figma 运行。ZCode 只需知道 URL，并按要求完成授权。

但“HTTP”不等于“服务器一定在云上”。例如 Figma 桌面 MCP 的地址可以是：

```text
http://127.0.0.1:3845/mcp
```

它仍然是 HTTP；只是服务器运行在我自己的电脑上。

所以：

> **本地 / 远程**回答的是“程序在哪里运行”；**stdio / HTTP**回答的是“客户端怎么跟它通信”。这两个维度不能混为一谈。

### 第三种：SSE——主要用于兼容旧式 HTTP 传输

旧版 MCP 的 SSE 传输通常通过持续的事件流接收消息，再用独立的 HTTP 请求发送消息。新版的 Streamable HTTP 也能按需使用 SSE 流，因此不能简单理解成“SSE 更实时”。

真正选哪个，取决于服务端提供了哪种端点：

```text
文档给 command + args        → 通常按 stdio 配
文档给 http(s)://.../mcp    → 通常按 HTTP 配
文档明确给旧式 SSE 端点      → 按 SSE 配
```

**传输方式不是一个可以随便切换的开关。** HTTP 授权失败，改成 SSE 并不会让原本不支持 SSE 的服务突然可用。

---

## 为什么官方 HTTP 报 403，第三方 stdio 却可以连接

第一次失败的信息是：

```text
Dynamic Client Registration rejected (HTTP 403): Forbidden
```

这里的关键词不是 `Figma`，甚至不是 `MCP`，而是：

```text
Dynamic Client Registration
```

它指的是 OAuth 的**动态客户端注册**。在正常读取设计稿之前，ZCode 尝试向授权系统注册自己，服务器在这个阶段返回了 403。

所以这个错误发生在：

```text
ZCode
  ↓ 尝试注册 OAuth 客户端
Figma 的授权服务
  ↓ 拒绝注册（403）
还没进入正常读取设计稿的阶段
```

它**不能**用来证明 Token 错误、Frame 链接错误、Node 版本错误，也不能只凭错误文本百分之百证明 Figma 拒绝的具体政策原因；只能确定注册请求被拒绝。

切换成 `figma-developer-mcp` 后，架构发生了变化：

```text
ZCode ── stdio ──> 第三方 Node.js 程序
                         │
                         └── Figma Token ──> Figma REST API
```

它不是“修好了官方 OAuth”，而是**改走另一条接入路径**：第三方程序用个人访问令牌调用 REST API，不再依赖之前那次远程 MCP 的动态客户端注册。

以后排障要先问：**失败发生在链路的哪一段？**

---

## 新问题：选了 stdio，为什么还会有 `spawn ENOTDIR`

`stdio` 的前提是：ZCode 必须先成功启动本地程序。

可以粗略把这一步理解为 Node.js 的：

```js
spawn("npx", ["-y", "figma-developer-mcp", "--stdio"]);
```

这里的 `spawn` 是启动子进程；`npx` 是要启动的命令；后面的数组是参数。

如果连子进程都没成功创建，那 MCP 的输入输出通道就不存在，更谈不上调用 Figma API。

我遇到的是：

```text
spawn ENOTDIR
```

`ENOTDIR` 的含义是：**某个被当作目录使用的路径组件实际上不是目录**。它属于进程启动阶段的路径错误，但仅凭这一行无法断定究竟是可执行文件路径、工作目录 `cwd`，还是其他路径处理出了问题。

还需要区分另一个常见错误：

```text
ENOENT：常见于文件或路径不存在、找不到可执行命令
ENOTDIR：路径中的某部分本应是目录，实际却不是
```

这两个错误不等价。不能看到任何 `spawn` 报错，就直接断言“系统没找到 npx”。

---

## `command: "npx"` 没有完整路径时，究竟怎么找

这是这次最值得沉淀的部分。

假设配置是：

```json
{
  "command": "npx"
}
```

这里没有提供绝对路径。ZCode 所使用的进程启动机制，一般会根据**启动环境中的 `PATH`** 搜索可执行程序。

假设它拿到的是：

```bash
PATH="/usr/local/bin:/usr/bin:/bin"
```

这里非常容易看错：它**不是一条很长的路径**。

冒号 `:` 是目录分隔符，拆开后是：

```text
1. /usr/local/bin
2. /usr/bin
3. /bin
```

要执行 `npx` 时，可以把查找过程想象成：

```text
/usr/local/bin/npx  ── 找到可执行文件？
        │ 否
        ▼
/usr/bin/npx        ── 找到可执行文件？
        │ 否
        ▼
/bin/npx            ── 找到可执行文件？
```

**按照顺序查找，找到符合条件的可执行程序，通常就停止搜索，不再继续往后找。**

但这个停止只针对**本次要找的命令**：

```text
执行 node → 从 PATH 头部开始查找 node
执行 git  → 重新从 PATH 头部开始查找 git
执行 npx → 重新从 PATH 头部开始查找 npx
```

不是“第一个目录里找到过任何一个程序，后面就永远不查了”。

这也解释了为什么**PATH 的顺序会影响使用哪个 Node 版本**：如果 Node 14 与 Node 22 的 `bin` 都在 PATH 中，通常排在前面的 `node` 会先被找到。

---

## 既然 `command` 都写了绝对路径，为什么还需要 `PATH`

后来我改成了类似这样的配置：

```json
{
  "command": "/Users/<用户名>/.nvm/versions/node/v22.23.2/bin/npx",
  "env": {
    "PATH": "/Users/<用户名>/.nvm/versions/node/v22.23.2/bin:/usr/local/bin:/usr/bin:/bin"
  }
}
```

直觉上的反问是：

> 我不是已经告诉 ZCode `npx` 在哪里了吗？为什么又要告诉它一堆目录？

答案在于：**启动 npx 和 npx 自己运行，是两个不同的问题。**

### 第一次：ZCode 找到 `npx`

```json
"command": "/Users/<用户名>/.nvm/versions/node/v22.23.2/bin/npx"
```

这是绝对路径。对“定位这个 npx 文件”而言，不必通过 PATH 去搜索它。

### 第二次：`npx` 需要找到执行自己的 Node.js

在常见的 npm/npx 安装形式中，入口脚本会有类似的第一行：

```bash
#!/usr/bin/env node
```

它的意思可以粗略理解成：**让 `/usr/bin/env` 去找到 `node`，用它执行当前脚本。**

这个 `node` 没有绝对路径，因此通常还要依赖 PATH：

```text
ZCode
  │
  │ command 使用绝对路径
  ▼
找到 npx 脚本
  │
  │ #!/usr/bin/env node
  ▼
根据 PATH 找到 node
  │
  ▼
Node.js 执行 npx
  │
  ▼
npx 再启动 figma-developer-mcp
```

所以这里的两项配置分别在回答：

```text
command：这一次具体启动哪个程序？
PATH：当进程需要按名字寻找其他程序时，去哪些目录找？
```

`PATH` 甚至还可能影响 `npx` 后续启动的其他子进程，不止 `node` 一个。

**但 PATH 不是必填项。** 如果 ZCode 原本继承的 PATH 就能找到正确的 Node.js，只写 `command` 的绝对路径也可能成功。显式设置 PATH，只是把对环境的依赖写出来，减少不同启动方式造成的不确定性。

---

## 为什么终端能找到 Node 22，桌面应用却不一定

我一开始运行：

```bash
which npx
```

得到的是 Node 14 的位置。随后：

```bash
nvm install 22
nvm use 22
which npx
which node
```

终端显示 `npx` 和 `node` 都位于 Node 22 的目录。

这不代表 ZCode 此时就一定使用 Node 22。

原因在于，`nvm use 22` 主要是在**当前 Shell 环境**里调整 PATH 等设置；而从 macOS Dock / Finder 启动的桌面应用，未必读取与终端相同的 Shell 初始化文件。

可以这样理解：

```text
终端进程
  └── 经过 nvm 初始化后的 PATH
        └── which node → Node 22

ZCode 进程
  └── 它自己继承 / 设置的 PATH
        └── 可能找不到 node，或找到另一个版本
```

因此：

> **`which node` 告诉我的，是当前终端环境会找到什么；它不自动等于另一个进程实际使用的环境。**

`nvm alias default 22` 可以设置新 Shell 常用的默认版本，但也不意味着 Dock 启动的应用会自动加载 nvm。

---

## 回到这次：最终能用的配置是什么

下面是**可迁移模板**。其中 `<...>` 必须替换成真实值；普通 JSON 的 `command` 不保证会自动展开 `~` 或 `$HOME`。不要把真实 Token 保存进公开知识库。

```json
{
  "mcpServers": {
    "figma": {
      "command": "<which npx 得到的绝对路径>",
      "args": [
        "-y",
        "figma-developer-mcp@latest",
        "--stdio"
      ],
      "env": {
        "FIGMA_API_KEY": "<在本机私有配置里填写 Token>",
        "PATH": "<Node 22 的 bin 绝对目录>:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
      }
    }
  }
}
```

再拆一下几个容易混在一起的字段：

```text
command  → 启动 npx
args     → 告诉 npx 运行什么包，以及给包传什么参数
-y       → 在 npx 需要确认下载安装时自动确认
--stdio  → 告诉这个 MCP 程序使用 stdio 模式（具体参数以安装版本为准）
env      → 为启动的进程提供环境变量
Token    → MCP 程序请求 Figma REST API 时使用的凭证
PATH     → 供进程查找 node 等可执行程序
```

注意：`@latest` 会随着时间变化。长期固定工作环境时，应考虑改成经过验证的具体版本。

还有一个排障结论需要保持严谨：**这次升级 Node、修改 `command`、设置 PATH 是一起完成的。连接成功只能说明组合配置有效，不能据此认定原始 `ENOTDIR` 必然由 Node 14 或 PATH 缺失单独导致。**

---

## 下次遇到类似问题，我应该怎么定位

与其看到“连接失败”就不停换配置，更合理的做法是按调用链逐层判断。

```text
第一层：远程 OAuth 注册失败？
  └── Dynamic Client Registration / 403
      → 看授权和客户端注册，不先查 Node / Token

第二层：本地进程无法启动？
  └── spawn ENOENT / ENOTDIR
      → 看 command、PATH、cwd、可执行文件和错误详情

第三层：进程已经启动，但 MCP 初始化失败？
  └── 看服务端日志、协议模式、参数、运行时

第四层：MCP 工具已加载，但读取设计稿失败？
  └── 看 Token 权限、文件访问权限、Frame 链接、API 返回
```

如果是进程启动问题，先在终端检查：

```bash
node -v
which node
which npx
npx -y figma-developer-mcp@latest --help
```

终端测试能帮我确认**这个 Shell 环境**是否能运行包，却不能直接证明 ZCode 的环境也一样。如果终端能跑、ZCode 不能跑，再检查 ZCode 实际使用的 `command`、`PATH`、工作目录 `cwd` 以及完整错误详情。

如果我真想知道这次**到底是哪一项修复了原错误**，就要在可恢复配置的前提下每次只改一个变量；而不是像这次一样同时修改 Node 版本、绝对路径与 PATH，然后把结果归功于某一个改动。

---

## 我的理解模型

以后看到一个 MCP 配置，我会先问三个问题，而不是直接记字段：

**第一：ZCode 连接的是谁？**

```text
官方远程服务器？
本机 HTTP 服务器？
还是它自己启动的 Node.js 子进程？
```

这决定该看 HTTP/OAuth，还是 stdio/进程启动。

**第二：连接和数据请求是不是同一回事？**

```text
ZCode → MCP Server 这一段怎么通信？
MCP Server → Figma 这一段又怎么请求？
```

这能防止把官方 OAuth 的 403、子进程启动失败、Figma API Token 错误混成一类问题。

**第三：进程到底是怎么被找到并运行的？**

```text
command = 找到本次要启动的 npx
               ↓
npx 的解释器 = 可能再通过 PATH 找 node
               ↓
Node.js 运行 MCP 程序
               ↓
MCP 程序建立 stdio 通信
               ↓
MCP 程序请求 Figma API
```

其中 `PATH` 是一张按冒号分隔、**有先后顺序的目录清单**。每次按命令名寻找可执行文件时，从前往后搜索，通常找到就停。

---

## 一句话总结

**一次“ZCode 连接 Figma”不是一个动作，而是一条跨越客户端、子进程、协议和外部 API 的调用链。**

`command` 决定最初启动谁；`PATH` 决定后续按名字去哪里找程序；`stdio/HTTP/SSE` 决定客户端怎样和 MCP Server 通信；Figma Token 或 OAuth 决定 MCP Server 怎样获得数据访问权限。

以后遇到错误，先判断**在哪一层失败**，再排查那一层，而不是把所有“连接失败”都归结为同一个原因。
