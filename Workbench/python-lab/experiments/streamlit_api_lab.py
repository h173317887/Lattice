"""Streamlit（快速构建 Python 网页界面的库）聊天 API 学习实验。

运行方式：在本目录且已激活 .venv（Python 虚拟环境）后，执行：
    streamlit run streamlit_api_lab.py
"""

import streamlit as st


# st.title()（页面主标题）把一级标题写到浏览器页面顶部。
st.title("Streamlit 聊天 API 学习实验")

# st.caption()（次要说明文字）适合放标题下的补充说明。
st.caption("目标：理解聊天机器人示例中的 Streamlit API，而不是照搬聊天机器人。")

# st.write()（通用内容输出函数）可以显示 Markdown（轻量标记文本）、文字或数据。
st.write(
    "这个页面保留了聊天界面最关键的交互，但回复由本地函数生成，不会请求模型，也不会消耗 API_KEY（接口访问密钥）。"
)


def show_lesson(number, api_name, plain_explanation, when_to_use, key_point, example):
    """用统一格式展示一个 API 的学习卡片。"""
    st.write(f"## {number}. `{api_name}`")
    st.write(f"**人话：** {plain_explanation}")
    st.write(f"**什么时候用：** {when_to_use}")
    st.write(f"**关键点：** {key_point}")
    # st.code()（显示带语法高亮的代码块）只负责展示，不会执行字符串里的代码。
    st.code(example, language="python")


st.write("# 一、逐项认识原示例中的 Streamlit API")

show_lesson(
    "1",
    "import streamlit as st",
    "导入 Streamlit，并给它取一个简短别名 `st`。之后所有页面组件都从 `st` 开始调用。",
    "每个 Streamlit 页面文件的开头。",
    "`st` 不是特殊关键字，只是大家约定俗成的别名；也可以换名，但不建议。",
    "import streamlit as st",
)

show_lesson(
    "2",
    "st.title() / st.caption()",
    "前者显示醒目的页面标题，后者显示较小的补充文字。它们从上到下出现，和代码顺序一致。",
    "搭建页面开头，告诉用户这个页面是做什么的。",
    "Streamlit 会按脚本的执行顺序排版，不需要你手动操作 HTML（网页结构语言）。",
    'st.title("🤖 我的第一个 AI 助手")\nst.caption("基于豆包大模型")',
)

show_lesson(
    "3",
    "st.session_state",
    "它像这个浏览器标签页专属的小记事本，用来保存 `messages`（消息列表）等数据。",
    "用户输入后页面会重新执行，而你希望历史消息不丢失时。",
    "每次交互 Streamlit 都会从上到下重新运行脚本；没有它，刷新后的变量会回到初始值。",
    'if "messages" not in st.session_state:\n    st.session_state.messages = []',
)

show_lesson(
    "4",
    "st.chat_message()",
    "它创建一条聊天气泡的显示区域。`user`（用户）和 `assistant`（助手）会使用不同的视觉样式。",
    "重放历史消息，或立即显示刚发送的用户消息和助手回复时。",
    "它需要和 `with`（Python 上下文管理语法：把缩进代码放进一个临时区域）一起使用。",
    'with st.chat_message("user"):\n    st.write("你好")',
)

show_lesson(
    "5",
    "st.chat_input()",
    "它提供固定在页面底部的聊天输入框。用户按 Enter（回车键）提交后，才返回输入的文字。",
    "需要收集用户问题时。",
    "没有新输入时返回 `None`（空值），所以通常放在 `if`（条件判断）中。",
    'if prompt := st.chat_input("输入你的问题..."):\n    st.write(prompt)',
)

show_lesson(
    "6",
    "st.write()",
    "这是最通用的输出工具：文字、Markdown、表格和很多 Python 对象都能交给它显示。",
    "不知道该用哪个展示函数时，或在聊天气泡中显示一段普通文本时。",
    "它一次性显示完整内容；想让内容边生成边出现，要使用下一项 `st.write_stream()`。",
    'with st.chat_message("assistant"):\n    st.write("这是完整显示的一段回复。")',
)

show_lesson(
    "7",
    "st.write_stream()",
    "它接收一段一段产出文字的可迭代对象，并把文字逐段显示成打字机效果；最终还会返回完整文本。",
    "模型接口使用 `stream=True`（流式返回：生成一点就返回一点）时。",
    "要把它的返回值存回历史消息，否则下一次页面重新执行时，助手这轮回复会消失。",
    'full_response = st.write_stream(text_chunks(response))\nst.session_state.messages.append(\n    {"role": "assistant", "content": full_response}\n)',
)

st.write("# 二、原示例中容易混淆的分工")
st.write(
    "`stream=True`（模型接口的流式返回开关）来自 OpenAI 客户端，不是 Streamlit API。"
    "模型返回的 `response`（流式响应对象）负责不断给出文本片段；`st.write_stream()`（逐段写入页面的函数）负责把这些片段显示在网页上。"
)
st.code(
    "response = client.chat.completions.create(..., stream=True)\n"
    "full_response = st.write_stream(\n"
    "    chunk.choices[0].delta.content or \"\"\n"
    "    for chunk in response\n"
    ")",
    language="python",
)
st.write(
    "中间的 `for chunk in response`（遍历流式响应中的每个片段）是 Python 的生成器表达式，"
    "它把模型产出的每一小段文字交给 `st.write_stream()`。"
)

st.write("# 三、动手观察：不调用模型的本地聊天练习")
st.write(
    "在底部输入任意内容。你会看到 `st.chat_input()`（聊天输入框）返回内容、"
    "`st.session_state`（跨重新执行保存的数据字典）保存历史、"
    "以及 `st.write_stream()`（逐段写入页面的函数）展示本地生成的回复。"
)

# 初始化只在当前浏览器会话的第一次运行时执行，避免每次输入都清空历史。
if "lab_messages" not in st.session_state:
    st.session_state.lab_messages = []

# 先重放已经保存在会话中的消息，所以页面重新执行后仍能看到完整对话。
for message in st.session_state.lab_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def local_text_chunks(prompt):
    """模拟流式响应：每次 yield（一边计算一边产出一个值）一小段文本。"""
    parts = [
        "你刚输入的是：",
        f"“{prompt}”。\n\n",
        "这段回复没有调用模型，而是由 `local_text_chunks()`（本地文本片段生成函数）分段产出。\n\n",
        "观察页面：文字会陆续出现，这就是 `st.write_stream()` 的作用。",
    ]
    for part in parts:
        yield part


# walrus 运算符（海象运算符：在条件判断中同时赋值）把输入保存到 prompt（用户输入文本）。
if prompt := st.chat_input("输入一句话，观察聊天 API 如何协作..."):
    st.session_state.lab_messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        full_response = st.write_stream(local_text_chunks(prompt))

    st.session_state.lab_messages.append(
        {"role": "assistant", "content": full_response}
    )
