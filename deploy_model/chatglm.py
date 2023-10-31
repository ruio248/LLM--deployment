from transformers import AutoTokenizer, AutoModel
from typing import List, Tuple
from dotenv import load_dotenv
import os

load_dotenv("deploy_model/.env")
CHATGLM_PATH = os.getenv("CHATGLM_PATH")

class CHATGLM:
    
    def __init__(self, model_path: str = CHATGLM_PATH, tokenizer_path: str = CHATGLM_PATH):
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path,trust_remote_code=True)
    def get_response(self, message: str, history: List[Tuple[str, str]] = [],max_length=400,top_p=0.9,temperature=1) -> str:
        response, history = self.model.chat(self.tokenizer, message, history=history, max_length=max_length, top_p=top_p, temperature=temperature) 
        return response,history

if __name__ == "__main__":
    chatbot = CHATGLM()
    response,history=chatbot.get_response("阿斯顿马丁",[('你好', '你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。')])
    print(response)
    print(history)
    