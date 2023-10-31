import streamlit as st
import requests
import time
import redis
st.title("我的 API 可视化界面")

# 模型选择
model_choice = st.selectbox("请选择模型类型:", ["GPT3.5", "LLAMA2", "CHATGLM"])
st.write(f"你选择了 {model_choice} 模型")

# 用户输入
prompt = st.text_input("请输入提示：")
max_length = st.slider("最大生成长度：", min_value=100, max_value=1000, value=400)
top_p = st.slider("Top P:", min_value=0.0, max_value=1.0, value=0.9, format="%.2f")
temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.9, format="%.2f")
history = st.text_area("历史记录 (用换行分隔每条)：").split("\n")

# 输入API密钥
api_key = st.text_input('请输入API密钥:', type='password')
assert api_key is not None, "没有输入api_key"

# 调用API按钮
if st.button("提交到API"):
    # API端点
    url = "http://localhost:8000/deploy_llm"
    headers = {
        "Content-Type": "application/json",
        "api_key": api_key  
    }
    data = {
        "prompt": prompt,
        "history": history,
        "max_length ": max_length,
        "top_p": top_p,
        "temperature": temperature,
        "model_type": model_choice  # 把模型选择也传到API
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        task_id = response.json().get("task_id")
        
        # 轮询获取任务结果
        while True:
            result_url = f"http://localhost:8000/get_result/{task_id}"
            result_response = requests.get(result_url)
            if result_response.status_code == 200:
                result_data = result_response.json()
                if result_data.get("status") == "success":
                    st.write("响应：", result_data["result"])
                    break
                elif result_data.get("status") == "failed":
                    st.write("错误：", result_data.get("result"))
                    break
            time.sleep(1)  # 每秒检查一次
    else:
        st.write("错误：", response.text)

st.write("注意：确保API服务器正在运行并可从此机器访问。")

st.title('API调用界面')
