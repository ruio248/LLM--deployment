import json
import time
import requests
import threading

# API 地址
url = "http://localhost:8000/deploy_llm"

def get_ans(id):
    t0 = time.time()
    headers = {'Content-Type': 'application/json',"api_key": "123"}
    
    # 需要发送的数据
    data = {
        "prompt": "什么是拓扑材料",
        "history": [],
        # ... 其他可选参数
    }
    response = requests.post(url, json=data, headers=headers)
    print(id, '耗时为：', round(time.time() - t0, 2), 's,结果为：', response.text)

if __name__ == '__main__':
    # 计算三个线程的总耗时
    t0 = time.time()

    t1 = threading.Thread(target=get_ans, args=('线程1',))
    t2 = threading.Thread(target=get_ans, args=('线程2',))
    t3 = threading.Thread(target=get_ans, args=('线程3',))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print(f"总共消耗的时间为{round(time.time() - t0, 2)}")
