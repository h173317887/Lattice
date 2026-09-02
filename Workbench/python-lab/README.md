# Python Lab

## 项目目的

集中管理 Python（编程语言）相关的 Demo（演示程序）和验证代码。每个 Demo 可以独立运行，验证说明按主题拆分，避免所有内容堆在同一个文档中。

## 代码

- `experiments/main.py`：使用 OpenAI 兼容接口（遵循 OpenAI 接口格式的模型服务）发送第一条请求。
- `experiments/chatbot.py`：使用 Streamlit（快速构建 Python 网页界面的库）实现带历史记录和流式回复的聊天助手。
- `experiments/streamlit_api_lab.py`：在网页中逐项讲解聊天示例里的 Streamlit（快速构建 Python 网页界面的库）API（应用程序接口：库提供的可调用功能），并提供不调用模型的交互练习。
- `experiments/requirements.txt`：Python（编程语言）依赖。

## 验证说明

- [AIbook 快速开始验证](validation/aibook-quickstart.md)

## 运行方式

1. 在 `experiments/.env` 中配置 `API_KEY`（接口访问密钥）。
2. 执行 `pip install -r experiments/requirements.txt` 安装依赖。
3. 运行 `python experiments/main.py`，对照验证说明检查输出。
4. 运行 `streamlit run experiments/chatbot.py`，在浏览器中打开 Streamlit（快速构建 Python 网页界面的库）聊天页面。
5. 运行 `streamlit run experiments/streamlit_api_lab.py`，学习聊天页面所用的 Streamlit API（应用程序接口：库提供的可调用功能）。

## 资料入口

- [AIbook 快速开始](https://aibook.mvtable.com/docs/#module-0/quickstart)（AIbook 的入门操作说明）
