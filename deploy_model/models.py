# llm_deploy/models.py

from deploy_model import llama_chat, openai_api, chatglm

LLAMA2 = llama_chat.LLAMA2()
GPT3_5 = openai_api.OpenAIAPI()
CHATGLM = chatglm.CHATGLM()
