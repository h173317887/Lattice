# Lattice

Lattice 是一个以 Markdown（轻量标记文本格式）文件为核心的个人知识库。Markdown 文件是 Source of Truth（唯一可信的原始记录）；Obsidian（本地知识库工具）、Git（版本管理工具）、编辑器和 AI Agent（人工智能代理）只是操作这些文件的不同入口。

## 目录

| 目录 | 它回答的问题 | 内容类型 |
| --- | --- | --- |
| `Inbox/` | 我刚刚想到了什么？ | 未分类的即时想法。 |
| `Learning/` | 我要学什么？应该按什么顺序学？ | 较大领域的学习路线、阶段、依赖和进度。 |
| `Workbench/` | 这个具体概念到底是什么？ | 问题驱动的查证、实验和概念建立过程。 |
| `Projects.md` | 我的项目在哪里？ | 项目名称与 GitHub（代码托管平台）链接。 |
| `Knowledge/` | 我已经搞懂了什么？ | 经过认知验收的稳定结论。 |
| `Maps/` | 我的知识如何连接？ | 领域级知识导航。 |

## 内容流转

```text
Inbox / Learning
       |
       v
   Workbench
       |
       v
   Knowledge
       |
       v
      Maps

Projects.md（项目链接清单）独立记录真实项目的 GitHub（代码托管平台）链接。
```

- `Inbox/inbox.md`（唯一的临时捕获文件）只需直接追加一句想法；处理后删除原句。
- `Learning/`（学习路线区）只用于图形学、机器人学、Physical AI（具身智能与物理环境交互的人工智能）等需要持续、多阶段学习的领域。它只保留路线节点和相关 Workbench（问题研究）的链接。
- `Workbench/`（问题研究区）用于 `requestAnimationFrame`（浏览器动画帧调度接口）、Forward Kinematics（正向运动学）等具体概念或问题。研究过程允许不完整、推翻和实验记录。
- `Knowledge/`（长期知识区）只接收自己已经能解释、认可、理解原因和适用边界的结论。
- `Maps/`（知识导航图区）不复制正文，只在知识结构真正变化时更新导航。

## 文档格式

`Learning`（学习路线）固定使用以下章节：

```md
# <学习领域名称>

## Goal
## Roadmap
## Workbenches
## Progress
```

`Workbench`（问题研究）固定使用以下章节：

```md
# <主题 / 核心问题>

## Goal
## Questions
## Research
## Core Model
## Boundaries
## Open Questions
## Knowledge Candidates
```

详细的创建约束见 [AGENTS.md](AGENTS.md)。
