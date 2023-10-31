from build_celery import cel
from deploy_model.models import GPT3_5

@cel.task
def GPT3_5_infer(prompt,history,max_length,top_p,temperature):
    response, history = GPT3_5.get_response(prompt,history,max_length,top_p,temperature)
    return response, history