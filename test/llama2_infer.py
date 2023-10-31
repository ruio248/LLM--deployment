import torch
import transformers
from transformers import LlamaForCausalLM, LlamaTokenizer
import re
model = LlamaForCausalLM.from_pretrained(
    '/media/ruihao/机器学习/llama/llama_model/Llama-2-7b-chat-hf').half().cuda()
tokenizer = LlamaTokenizer.from_pretrained('/media/ruihao/机器学习/llama/llama_model/Llama-2-7b-chat-hf')
def format_prompt(history, message, system_prompt):
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    prompt = f"{B_INST} {B_SYS}{system_prompt}{E_SYS} "
    for user_msg, asst_msg in history:
        user_msg = str(user_msg).strip()
        asst_msg = str(asst_msg).strip()
        prompt += f"{user_msg} {E_INST} {asst_msg} </s><s> {B_INST} "

    message = str(message).strip()
    prompt += f"{message} {E_INST} "
    return prompt
SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

prompt = format_prompt(history=[], message='How much is the capacity in "Organic materials are competitive as anodes for Na-ion batteries (NIBs) due to the low cost, abundance, environmental benignity, and high sustainability. Herein, we synthesized three halogenated carboxylate-based organic anode materials to exploit the impact of halogen atoms (F, Cl, and Br) on the electrochemical performance of carboxylate anodes in NIBs. The fluorinated carboxylate anode, disodium 2, 5-difluoroterephthalate (DFTP-Na), outperforms the other carboxylate anodes with H, Cl, and Br, in terms of high specific capacity (212 mA h g–1), long cycle life (300 cycles), and high rate capability (up to 5 A g–1). As evidenced by the experimental and computational results, the two F atoms in DFTP reduce the solubility, enhance the cyclic stability, and interact with Na+ during the redox reaction, resulting in a high-capacity and stable organic anode material in NIBs. Therefore, this work proves that fluorinating carboxylate compounds is an effective approach to developing high-performance organic anodes for stable and sustainable NIBs"', system_prompt=SYSTEM_PROMPT)

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
max_gen_len = 4096
temperature = 0.6
top_p = 0.9
out = model.generate(
    **inputs,
    max_new_tokens=max_gen_len,
    temperature=temperature,
    top_p=top_p,
)
raw_response= tokenizer.decode(out[0])
# Split the string by "[/INST] "
response=re.search(r"\[/INST\](.*?)</s>",raw_response,re.DOTALL)
print(response.group(1))