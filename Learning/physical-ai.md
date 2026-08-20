# Physical AI

## Goal

能够为一个简单具身智能任务选择合适的坐标表示、仿真环境、机器人建模方式和学习方法，并能解释这些模块在“感知、决策、动作、物理反馈”闭环中的作用。

## Roadmap

### 1. Spatial Foundations（空间基础）

- [ ] [[coordinate-transform]]
- [ ] [[quaternion]]
- [ ] [[fk-vs-scene-graph]]

### 2. Simulation（仿真）

- [ ] Rigid Body Dynamics（刚体动力学）
- [ ] MuJoCo（物理仿真引擎）基础
- [ ] timestep（仿真时间步长）与稳定性

### 3. Robotics（机器人学）

- [ ] [[forward-kinematics]]
- [ ] Inverse Kinematics（逆向运动学）
- [ ] Jacobian（雅可比矩阵）

### 4. Robot Learning（机器人学习）

- [ ] Behavior Cloning（行为克隆）
- [ ] PPO（近端策略优化）

### 5. Isaac Sim（机器人仿真平台）

- [ ] 场景、机器人和传感器建模
- [ ] 将一个训练或控制实验跑通

## Workbenches

- [[fk-vs-scene-graph]]

## Progress

当前处于 Spatial Foundations（空间基础）阶段，先研究坐标变换与 FK（正向运动学）的关系。
