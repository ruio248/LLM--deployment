from celery import Celery,signals
from deploy_model.model_loader import ModelLoader
from dotenv import load_dotenv
import os
from model_infer import generate_output_gpt_3_5,generate_output_llama2,generate_output_chatglm

cel =Celery('celery_demo',broker='redis://127.0.0.1:6379/1',
            backend='redis://127.0.0.1:6379/2',)
print("cel对象创建成功")

load_dotenv(".env")
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")
OPENAI_URL = os.getenv("OPENAI_URL")
LLAMA2_PATH =os.getenv("LLAMA2_PATH")
CHATGLM_PATH = os.getenv("CHATGLM_PATH")


model_loader = None



@signals.worker_process_init.connect
def setup_model(signal, sender, **kwargs):
    global model_loader
    model_loader = ModelLoader(LLAMA2_PATH, CHATGLM_PATH)

@cel.task
def get_gpt_3_5_response(prompt,history,max_length,top_p,temperature,openai_key=OPENAI_APIKEY,openai_url=OPENAI_URL):
    response,history= generate_output_gpt_3_5(
        prompt,history,max_length,top_p,temperature,openai_key,openai_url
    )
    return response,history

@cel.task
def get_llama2_response(prompt,history,max_length,top_p,temperature):
    response,history= generate_output_llama2(
        prompt,history,max_length,top_p,temperature,model_loader.llama2_model,model_loader.llama2_tokenizer)
    return response,history

@cel.task
def get_chatglm_response(prompt,history,max_length,top_p,temperature):
    response,history= generate_output_chatglm(
        prompt,history,max_length,top_p,temperature,model_loader.chatglm_model,model_loader.chatglm_tokenizer
    )
    return response,history

