# Lattice 文档约束

解释代码或技术方案时，函数名、组件名、变量名、状态名、事件名、消息类型、英文缩写或技术术语首次出现时，必须在括号中补充中文解释。先用人话说明，再给出代码名或术语。

## 目录职责

- `Inbox/`（临时捕获区）只记录刚想到的内容。
- `Learning/`（学习路线区）只管理较大领域的路线、阶段、顺序、依赖和进度。
- `Workbench/`（问题研究区）只研究一个具体概念或问题。
- `Projects.md`（项目链接清单）只记录项目名称和 GitHub（代码托管平台）链接，不保存完整项目源码。
- `Knowledge/`（长期知识区）只保存已经完成认知验收的稳定结论。
- `Maps/`（知识导航图区）只保存领域级导航，不复制正文。

Learning（学习路线）回答“接下来应该学什么”；Workbench（问题研究）回答“这个具体概念到底是什么”。具体概念不能单独创建 Learning（学习路线）。Learning（学习路线）中只保留 Workbench（问题研究）的链接，不复制详细问题、资料或实验。

每个 Workbench（问题研究）主题使用 `Workbench/<topic>/README.md`（主题主文档）组织；需要验证的代码放在同一主题的 `experiments/`（实验目录）中，不创建全局实验目录。

## Learning 固定格式

```md
# <学习领域名称>

## Goal

## Roadmap

### 1. <阶段名称>

- [ ] <知识主题>

## Workbenches

- [[workbench-name]]

## Progress
```

`Goal`（目标）必须描述可验证的能力结果；`Roadmap`（路线图）必须体现学习依赖和顺序；不得在 Learning（学习路线）中记录详细资料、实验过程、概念解释或最终知识。

## Workbench 固定格式

```md
# <主题 / 核心问题>

## Goal

## Questions

- [ ] Q1：<问题>

## Research

### Q1：<问题>

查到：

- <资料、实验、现象或反例>

**Conclusion**

> <该问题的当前结论>

## Core Model

## Boundaries

## Open Questions

- [ ] <新问题>

## Knowledge Candidates

- [[knowledge-name]]
```

Research（研究记录）中的每一段必须服务于一个明确问题，可以记录资料、源码、实验、现象、反例和 AI（人工智能）讨论。每个问题下的 Conclusion（该问题的当前结论）直接回答该问题；不创建全局 `## Conclusions`（逐题结论汇总）章节。Core Model（核心模型）形成整体心智模型；研究完成后提炼 Knowledge（长期知识），不要无限追加。

## 其他规则

- Inbox（临时捕获区）默认只有 `Inbox/inbox.md`，直接追加一句，处理后删除。
- Demo（验证结论的最小实验）只放在对应主题旁边；不创建全局 Demo 目录。
- 不为展示结构创建额外文档或额外目录。
