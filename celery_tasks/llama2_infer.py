from build_celery import cel
from deploy_model.models import LLAMA2

@cel.task
def LLAMA2_infer(prompt,history,max_length,top_p,temperature):
    response, history = LLAMA2.get_response(prompt,history,max_length,top_p,temperature)
    return response, history


