from celery import Celery

cel =Celery('celery_demo',broker='redis://127.0.0.1:6379/1',
            backend='redis://127.0.0.1:6379/2',
            include=['celery_tasks.llama2_infer','celery_tasks.chatglm_infer','celery_tasks.gpt3_5_infer'])
print("cel对象创建成功")