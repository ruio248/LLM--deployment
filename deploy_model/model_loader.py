import os
from transformers import AutoTokenizer, AutoModel
from transformers import LlamaForCausalLM, LlamaTokenizer

class ModelLoader:
    def __init__(self, llama2_path: str,chatglm_path: str):
        self.llama2_path = llama2_path
        self.chatglm_path = chatglm_path
        self.llama2_model,self.chatglm_model = self._load_model()
        self.llama2_tokenizer = LlamaTokenizer.from_pretrained(llama2_path)
        self.chatglm_tokenizer = AutoTokenizer.from_pretrained(chatglm_path,trust_remote_code=True)
        
    def _load_model(self):
        llama2_model=LlamaForCausalLM.from_pretrained(self.llama2_path).half().cuda()
        chatglm_model = AutoModel.from_pretrained(self.chatglm_path,trust_remote_code=True).quantize(8).half().cuda()  #八位精度量化
        llama2_model.eval()
        chatglm_model.eval()
        return llama2_model,chatglm_model