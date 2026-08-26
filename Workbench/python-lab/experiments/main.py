import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# 豆包/DeepSeek/通义千问都支持OpenAI兼容格式
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3"  # 豆包接入点
    # 通义千问：base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    # DeepSeek：base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="ep-20260825194133-prddb",  # 豆包模型名
    # model="deepseek-chat"  # DeepSeek
    # model="qwen-turbo"     # 通义千问
    messages=[
        {"role": "system", "content": "你是一个友好的AI助手"},
        {"role": "user", "content": "用三句话解释什么是RAG技术"}
    ]
)

print(response.choices[0].message.content)