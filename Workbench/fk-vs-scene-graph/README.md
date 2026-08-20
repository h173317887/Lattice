# FK 与 Scene Graph 的关系

## Goal

弄清 Forward Kinematics（正向运动学）和 Scene Graph（场景图）是否都在处理层级坐标变换；能够准确说出两者共有的计算模型，以及 Joint Constraint（关节约束）和 DH Parameter（Denavit-Hartenberg 参数，一种描述机器人连杆关系的约定）带来的差异。

## Questions

- [ ] Q1：两者是否都通过父节点到子节点的变换组合，得到子节点的世界坐标？
- [ ] Q2：FK（正向运动学）相比普通 Scene Graph（场景图）多了哪些关节、连杆和自由度约束？
- [ ] Q3：DH Parameter（Denavit-Hartenberg 参数）解决什么建模问题？它是计算所必需的，还是一种约定？

## Research

每个问题都在同一处记录查到的关键证据，并紧接着写出当前结论。

### Q1：层级变换是否相同？

查到：

- [ ] 在 `experiments/transform-demo/`（变换实验目录）中画出父节点、子节点和世界坐标的关系。
- [ ] 用矩阵或伪代码分别写出普通层级变换与两段连杆的坐标计算。

**Conclusion**

> 待研究。

### Q2：约束从哪里出现？

查到：

- [ ] 列出普通场景节点与机器人关节各自允许改变的属性。
- [ ] 用一个两关节机械臂示例观察关节角度变化如何影响末端位置。

**Conclusion**

> 待研究。

### Q3：为什么使用 DH Parameter？

查到：

- [ ] 查阅 DH Parameter（Denavit-Hartenberg 参数，一种描述机器人连杆关系的约定）如何描述相邻连杆。
- [ ] 比较“直接写变换矩阵”和“使用 DH Parameter（Denavit-Hartenberg 参数）”时各自保留的信息。

**Conclusion**

> 待研究。

## Core Model

待研究。

## Boundaries

待研究。

## Open Questions

- [ ] Inverse Kinematics（逆向运动学）与 Scene Graph（场景图）的关系是什么？

## Knowledge Candidates

- [[coordinate-transform]]
- [[forward-kinematics]]
