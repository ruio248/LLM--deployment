import requests

# API 地址
url = "http://localhost:8000/deploy_llm"


# 包含 API 密钥的 headers
headers = {
    "Content-Type": "application/json",
    "api_key": "123"
}

# 需要发送的数据
# 这里model type 可以选择为 GPT3.5，LLAMA2，CHATGLM
data = {
    "prompt": "Hello",
    "history": [],
    "model_type": "chatglm",
    # ... 其他可选参数
}

response = requests.post(url, json=data, headers=headers)

# 输出响应
print(response.text)


