from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi import Header
import redis
from celery_worker import get_gpt_3_5_response,get_llama2_response,get_chatglm_response
from celery_worker import cel
from celery.result import AsyncResult
#从redis服务器加载api_key 
def get_api_keys_from_redis():
    return [key.decode('utf-8') for key in redis_client.smembers("api_keys")]
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
API_KEYS = get_api_keys_from_redis()
print(f"api_keys为{API_KEYS}") 

def verify_api_key(api_key: str = Header(None, alias="api_key")):
    API_KEYS = get_api_keys_from_redis()
    print(f"Received API key: {api_key}")
    print(f"Valid API keys: {API_KEYS}")
    if api_key in API_KEYS:
        return api_key
    raise HTTPException(status_code=400, detail="Invalid API Key")

app = FastAPI()
@app.post("/deploy_llm")
async def create_item(request: Request, api_key: str = Depends(verify_api_key)):
    json_post = await request.json()
    prompt = json_post.get('prompt')
    history = json_post.get('history')
    max_length = json_post.get('max_length')
    top_p = json_post.get('top_p')
    temperature = json_post.get('temperature')
    model_type = json_post.get('model_type')
    if model_type == 'GPT3.5':
        task = get_gpt_3_5_response.delay(prompt,history,max_length,top_p,temperature)  # 使用.delay()来异步调用
    elif model_type == 'LLAMA2':
        task = get_llama2_response.delay(prompt,history,max_length,top_p,temperature) 
    elif model_type == 'CHATGLM':
        task = get_chatglm_response.delay(prompt,history,max_length,top_p,temperature) 
    else:
        task = get_gpt_3_5_response.delay(prompt,history,max_length,top_p,temperature) 

    return {"status": "Task started", "task_id": task.id}

@app.get("/get_result/{task_id}")
async def get_result(task_id: str):
    task = cel.AsyncResult(task_id)  # 应该怎么导
    if task.state == 'PENDING':
        response = {"status": "pending"}
    elif task.state != 'FAILURE':
        response = {"status": "success", "result": task.result}
    else:
        response = {"status": "failed", "result": str(task.result)}
    return response

