"""Streamlit (快速构建 Python 网页界面的库) 聊天助手实验。

运行方式：在本目录且已激活 .venv（Python 虚拟环境）后，执行：
    streamlit run chatbot.py
"""

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# load_dotenv()（读取 .env 文件中的环境变量）会让 API_KEY 不必写进代码。
load_dotenv()

# OpenAI（模型服务客户端）也可连接遵循 OpenAI 请求格式的豆包接口。
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

# 这里复用 main.py（基础接口实验）中已经验证可用的推理接入点标识。
MODEL_ID = "ep-20260825194133-prddb"


def text_chunks(response):
    """从流式响应中取出非空文本片段，供 st.write_stream() 逐段显示。"""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content


# st.title()（页面主标题）和 st.caption()（较小的说明文字）写入页面顶部。
st.title("🤖 我的第一个 AI 助手")
st.caption("基于豆包大模型和 Streamlit")

# st.session_state（跨页面重新执行时保留的数据字典）存放完整对话记录。
# Streamlit 每次输入都会重新运行本文件，所以必须只在第一次创建 messages（消息列表）。
if "messages" not in st.session_state:
    st.session_state.messages = []

# st.chat_message()（聊天消息容器）按角色显示每一条历史消息。
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])  # st.write()（通用内容输出函数）显示文本。

# st.chat_input()（固定在页面底部的聊天输入框）在用户提交时返回输入文字。
if prompt := st.chat_input("输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 先立即显示用户消息，再开始等待模型回复，界面不会显得没有响应。
    with st.chat_message("user"):
        st.write(prompt)

    # stream=True（流式返回：模型生成一点就返回一点）配合 write_stream() 实现打字机效果。
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "你是一个专业的 AI 助手，回答简洁准确。"},
                *st.session_state.messages,
            ],
            stream=True,
        )
        # st.write_stream()（逐段写入页面的函数）返回本次完整回复，方便存入历史记录。
        full_response = st.write_stream(text_chunks(response))

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
