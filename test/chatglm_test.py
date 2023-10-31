from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("/media/ruihao/机器学习/ChatGLM-6B/model/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("/media/ruihao/机器学习/ChatGLM-6B/model/chatglm-6b", trust_remote_code=True).half().cuda()
model = model.eval()
response, history = model.chat(tokenizer, "你好", history=[])
print(response)
