import re
from transformers import LlamaForCausalLM, LlamaTokenizer
from typing import List, Tuple
from dotenv import load_dotenv
import os

load_dotenv("deploy_model/.env")
LLAMA2_PATH = os.getenv("LLAMA2_PATH")
print(LLAMA2_PATH)
class LLAMA2:

    def __init__(self, model_path: str = LLAMA2_PATH, tokenizer_path: str = LLAMA2_PATH):
        self.model = LlamaForCausalLM.from_pretrained(model_path).half().cuda()
        self.model.eval()
        self.tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)
        self.SYSTEM_PROMPT = """\
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

    def format_prompt(self, history: List[Tuple[str, str]], message: str) -> str:
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

        prompt = f"{B_INST} {B_SYS}{self.SYSTEM_PROMPT}{E_SYS} "
        for user_msg, asst_msg in history:
            user_msg = str(user_msg).strip()
            asst_msg = str(asst_msg).strip()
            prompt += f"{user_msg} {E_INST} {asst_msg} </s><s> {B_INST} "

        message = str(message).strip()
        prompt += f"{message} {E_INST} "
        return prompt

    def get_response(self, message: str, history: List[Tuple[str, str]] = [],max_length=400,top_p=0.9,temperature=1) -> str:
        prompt = self.format_prompt(history, message)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        out = self.model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=temperature,
            top_p=top_p,
        )
        raw_response = self.tokenizer.decode(out[0])
        matches = re.findall(r"\[/INST\](.*?)</s>", raw_response, re.DOTALL)
        if matches:
            last_match = matches[-1].strip()
            response = last_match
        else:
            response = ""

        history.append((message, response))
        return response, history
if __name__== "__main__":
    assistant = LLAMA2()
    history=[('阿斯顿马丁', '阿斯顿马丁(Aston Martin)是一家英国汽车制造商，成立于1937年，总部位于伦敦。阿斯顿马丁以生产高性能、豪华和优雅的汽车而著称，其标志性的车型包括 Vantage、醒狮、S级和马丁GT等。阿斯顿马丁的汽车产品包括轿车、跑车、SUV和奢华SUV等不同类型，在全球范围内销售。')]
    response,history = assistant.get_response("卡布大是谁", history)
    print(response)
    print(history)

