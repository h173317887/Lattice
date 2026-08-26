# Python `with`：从资源管理到上下文管理

## 先看一个让我产生疑问的例子

在 Streamlit 里经常能看到：

```python
with st.chat_message("user"):
    st.write("你好")
```

直觉上会有一个疑问：

> `with` 明明是 Python 语法，`st` 只是第三方库。为什么 `with` 可以让 `st.write()` 的内容自动进入 `st.chat_message()` 创建的聊天区域？

理解这个问题，需要先理解 Python 的 **上下文管理器（Context Manager）**。

---

## `with` 最初解决什么问题

有一类操作天然具有这样的生命周期：

```text
准备
↓
使用
↓
清理
```

例如文件：

```python
f = open("a.txt")
f.write("hello")
f.close()
```

问题在于，如果中途发生异常：

```python
f = open("a.txt")

1 / 0

f.close()
```

`f.close()` 就可能无法执行。

传统写法需要：

```python
f = open("a.txt")

try:
    f.write("hello")
finally:
    f.close()
```

因此 Python 提供了：

```python
with open("a.txt") as f:
    f.write("hello")
```

它表达的是：

```text
进入某个上下文
↓
执行一段代码
↓
无论正常结束还是发生异常，都退出上下文
```

最早最典型的使用场景包括：

* 打开 / 关闭文件
* 获取 / 释放锁
* 建立 / 关闭连接
* 开启 / 提交或回滚事务

所以 `with` 最容易理解成：

> **管理一段具有“进入”和“退出”生命周期的代码。**

---

## `with` 背后的协议

`with` 后面可以写一个对象，也可以写一个表达式。真正需要支持上下文管理协议的，是这个表达式最终返回的对象。

例如：

```python
with st.chat_message("user"):
    st.write("你好")
```

这里 `with` 管理的不是 `st`（Streamlit 主模块对象）本身，而是 `st.chat_message("user")` 返回的对象。这个返回对象需要实现下面两个特殊方法：

```python
__enter__()
__exit__()
```

直接写对象时也是同样的规则：

```python
with obj:
    ...
```

其中 `obj` 本身就是被管理的对象。

例如：

```python
class Demo:
    def __enter__(self):
        print("进入")

    def __exit__(self, exc_type, exc_value, traceback):
        print("退出")
```

使用：

```python
with Demo():
    print("执行代码")
```

输出：

```text
进入
执行代码
退出
```

因此：

```python
with obj:
    do_something()
```

可以粗略理解为：

```python
obj.__enter__()

try:
    do_something()
finally:
    obj.__exit__(...)
```

实际实现细节更复杂，但理解 `with` 时，这个模型已经足够。

---

## `__enter__()` 是什么

`__enter__()` 会在进入 `with` 代码块之前调用。

```python
class Demo:
    def __enter__(self):
        print("准备环境")

    def __exit__(self, exc_type, exc_value, traceback):
        print("恢复环境")
```

执行：

```python
with Demo():
    print("hello")
```

顺序就是：

```text
__enter__()
↓
执行 with 内部代码
↓
__exit__()
```

所以：

```text
__enter__
```

可以理解成：

> **建立接下来这段代码运行所需要的上下文。**

---

## `__exit__()` 是什么

`__exit__()` 会在离开 `with` 时调用。

即使代码块内部发生异常，它通常依然会执行：

```python
with Demo():
    print("hello")
    1 / 0
```

大致过程：

```text
进入
hello
退出
ZeroDivisionError
```

这也是 `with` 非常适合资源清理的原因。

`__exit__()` 还会收到异常信息：

```python
def __exit__(self, exc_type, exc_value, traceback):
    ...
```

其中：

```text
exc_type
```

是异常类型。

```text
exc_value
```

是具体异常。

```text
traceback
```

是调用栈信息。

如果没有异常，这些值一般是 `None`。

---

## `as xxx` 又是什么

例如：

```python
with open("a.txt") as f:
    ...
```

这里的 `f` 并不是简单等于 `open("a.txt")` 返回的对象本身，而是接收这个对象的 `__enter__()` 返回值：

```python
open("a.txt")
```

更准确地说：

```python
obj = open("a.txt")

f = obj.__enter__()
```

也就是说：

> `as` 接收到的是 `__enter__()` 的返回值。

例如：

```python
class Demo:
    def __enter__(self):
        return "hello"

    def __exit__(self, exc_type, exc_value, traceback):
        pass
```

那么：

```python
with Demo() as value:
    print(value)
```

输出：

```text
hello
```

很多上下文管理器会：

```python
def __enter__(self):
    return self
```

所以通常看起来像是直接拿到了原来的对象。

---

## 为什么 `with st.chat_message()` 不需要接收返回值

Streamlit：

```python
with st.chat_message("user"):
    st.write("你好")
```

虽然没有：

```python
message = st.chat_message("user")
```

但 Python 内部依然会拿到 `st.chat_message()` 返回的对象。

可以粗略理解成：

```python
obj = st.chat_message("user")

obj.__enter__()

try:
    st.write("你好")
finally:
    obj.__exit__(...)
```

所以：

> **不是没有返回值，而是 `with` 自己使用了这个返回对象。**

只有当我们还需要在代码块里直接使用 `__enter__()` 的返回值时，才需要：

```python
with xxx as value:
    ...
```

---

## Streamlit 为什么可以把内容放进聊天框

这是最有意思的一部分。

`with` 本身完全不知道：

```text
聊天框
Streamlit
UI
```

这些概念。

它只知道：

```text
调用 __enter__()
执行代码
调用 __exit__()
```

真正决定行为的是 Streamlit。

可以粗略想象 `st.chat_message()` 返回的对象内部类似：

```python
class ChatMessage:
    def __enter__(self):
        # 把当前 Streamlit 的默认输出容器
        # 临时修改成这个聊天消息容器
        set_current_container(self)

    def __exit__(self, exc_type, exc_value, traceback):
        # 恢复之前的输出容器
        restore_previous_container()
```

于是：

```python
with st.chat_message("user"):
    st.write("你好")
    st.button("按钮")
```

大致变成：

```text
进入 chat_message
↓
Streamlit 当前输出目标 = chat_message

st.write("你好")
↓
输出到 chat_message

st.button("按钮")
↓
输出到 chat_message

退出 with
↓
恢复之前的输出目标
```

因此，真正起作用的不是：

```python
with
```

“知道要把内容放进聊天框”。

而是：

> **Streamlit 利用了 `with` 提供的上下文管理机制，在进入和退出代码块时修改自己的内部状态。**

---

## 不使用 `with` 也可以

Streamlit 也可以这样：

```python
message = st.chat_message("user")

message.write("你好")
```

这里的逻辑非常直接：

```text
拿到聊天容器
↓
调用聊天容器自己的 write
```

而：

```python
with st.chat_message("user"):
    st.write("你好")
```

表达的是另一种思路：

```text
临时把这个聊天容器设置成默认输出位置
↓
接下来普通的 st.xxx 都默认写进去
```

当内部内容很多时：

```python
with st.chat_message("user"):
    st.write("你好")
    st.image(...)
    st.button("确认")
```

这种写法会非常自然。

---

## 这算不算第三方库的“骚操作”

某种程度上可以说设计得很巧，但它并不是 hack。

`with` 最初最常见的用途确实是：

```text
打开资源
↓
使用资源
↓
释放资源
```

但 Python 对它的正式抽象其实是：

```text
Context Manager
上下文管理器
```

也就是：

> **在某段代码执行期间，临时建立一种环境，执行结束之后再恢复。**

所以现在很多库都会这么使用：

```python
with open("a.txt"):
    ...
```

文件上下文。

```python
with lock:
    ...
```

锁上下文。

```python
with database.transaction():
    ...
```

数据库事务上下文。

```python
with torch.no_grad():
    ...
```

临时关闭梯度计算。

```python
with st.sidebar:
    ...
```

临时改变 Streamlit 输出位置。

```python
with st.chat_message("user"):
    ...
```

临时改变 Streamlit 输出容器。

这些本质上其实是同一种模式。

---

## 我的理解模型

以后看到：

```python
with XXX:
    ...
```

不要把它记成：

> `with` 是用来打开文件的。

更好的理解是：

```text
XXX.__enter__()
↓
建立某种临时上下文

执行缩进代码

XXX.__exit__()
↓
退出 / 清理 / 恢复上下文
```

至于：

```text
进入时做什么
退出时做什么
```

由 `XXX` 自己决定。

因此：

```python
with st.chat_message("user"):
    st.write("你好")
```

最准确的理解是：

```text
进入 Streamlit 的 chat_message 上下文
↓
临时把当前 UI 输出位置切换到这个聊天消息容器
↓
执行 st.write()
↓
退出 chat_message 上下文
↓
恢复之前的 UI 输出位置
```

---

## 一句话总结

`with` 本身并不知道文件、数据库、锁或者 Streamlit。

它只提供了一套：

```text
__enter__()
↓
执行代码
↓
__exit__()
```

的语言协议。

**第三方库通过实现这套协议，决定“这段代码运行期间处于什么上下文”。**

这也是为什么 Python 原生语法可以如此自然地和第三方库结合。
