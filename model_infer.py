import time
import torch
import functools
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import json
import re
from typing import List, Tuple
import ast
def time_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        return (result, exec_time)
    return wrapper


def memory_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        result, exec_time = func(*args, **kwargs)
        peak_mem = torch.cuda.max_memory_allocated()
        peak_mem_consumption = peak_mem / 1e9
        return peak_mem_consumption, exec_time, result
    return wrapper


def generate_output_gpt_3_5(prompt:str,history:List[Tuple[str, str]],max_length,top_p,temperature,OPENAI_APIKEY,OPENAI_URL):
        headers = {
            "Authorization": f"Bearer {OPENAI_APIKEY}",
            "Content-Type": "application/json",
        }

        messages = [{"role": "user", "content": prompt}]
        history = ast.literal_eval(history)
        if len(history) !=0:
            for h in history:
                messages.append({"role": "user", "content": h[-2]})
                messages.append({"role": "assistant", "content": h[-1]})

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': messages
        }

        if max_length is not None:
            data['max_tokens'] = max_length
        if top_p is not None:
            data['top_p'] = top_p
        if temperature is not None:
            data['temperature'] = temperature

        response_raw = requests.post(OPENAI_URL, headers=headers, data=json.dumps(data))
        
        # Check if the request was successful
        if response_raw.status_code != 200:
            raise Exception(f"Error: {response_raw.text}")

        response_json = response_raw.json()
        response = response_json['choices'][0]['message']['content']
        # Update the history with the new message
        history.append((prompt, response))
        return response,history


def generate_output_llama2(message:str,history:List[Tuple[str, str]],max_length,top_p,temperature,model,tokenizer):
    SYSTEM_PROMPT = """\
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
   
    prompt = f"{B_INST} {B_SYS}{SYSTEM_PROMPT}{E_SYS} "
    history = ast.literal_eval(history)
    if len(history) != 0:
        for user_msg, asst_msg in history:
            user_msg = str(user_msg).strip()
            asst_msg = str(asst_msg).strip()
            prompt += f"{user_msg} {E_INST} {asst_msg} </s><s> {B_INST} "    
    message = str(message).strip()
    prompt += f"{message} {E_INST} "
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device) 
    out = model.generate(
        **inputs,
        max_new_tokens=max_length,
        temperature=temperature,
        top_p=top_p,
    )
    raw_response = tokenizer.decode(out[0])
    matches = re.findall(r"\[/INST\](.*?)</s>", raw_response, re.DOTALL)
    if matches:
        last_match = matches[-1].strip()
        response = last_match
    else:
        response = ""
    
    history.append((message, response))
    return response, history


def generate_output_chatglm(prompt:str,history:List[Tuple[str, str]],max_length,top_p,temperature,model,tokenizer):
    raw_history= ast.literal_eval(history)
    response, history = model.chat(tokenizer, prompt, history=raw_history, max_length=max_length, top_p=top_p, temperature=temperature) 
    return response, history