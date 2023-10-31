from build_celery import cel
from deploy_model.models import CHATGLM

@cel.task
def CHATGLM_infer(prompt,history,max_length,top_p,temperature):
    response, history = CHATGLM.get_response(prompt,history,max_length,top_p,temperature)
    return response,history