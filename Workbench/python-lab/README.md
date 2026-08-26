# Python Lab

## 项目目的

集中管理 Python（编程语言）相关的 Demo（演示程序）和验证代码。每个 Demo 可以独立运行，验证说明按主题拆分，避免所有内容堆在同一个文档中。

## 代码

- `experiments/main.py`：使用 OpenAI 兼容接口（遵循 OpenAI 接口格式的模型服务）发送第一条请求。
- `experiments/requirements.txt`：Python（编程语言）依赖。

## 验证说明

- [AIbook 快速开始验证](validation/aibook-quickstart.md)

## 运行方式

1. 在 `experiments/.env` 中配置 `API_KEY`（接口访问密钥）。
2. 执行 `pip install -r experiments/requirements.txt` 安装依赖。
3. 运行 `python experiments/main.py`，对照验证说明检查输出。

## 资料入口

- [AIbook 快速开始](https://aibook.mvtable.com/docs/#module-0/quickstart)（AIbook 的入门操作说明）
