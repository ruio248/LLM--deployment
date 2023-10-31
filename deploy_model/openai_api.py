import requests  # Add this line to import the module
import json
from dotenv import load_dotenv
import os

load_dotenv("deploy_model/.env")
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")
OPENAI_URL = os.getenv("OPENAI_URL")

class OpenAIAPI:
    def __init__(self):
        self.api_key = OPENAI_APIKEY
        self.url = OPENAI_URL

    def get_response(self, prompt, history=None, max_tokens=None, top_p=None, temperature=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = [{"role": "user", "content": prompt}]

        if history:
            for h in history:
                messages.append({"role": "user", "content": h[-2]})
                messages.append({"role": "assistant", "content": h[-1]})

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': messages
        }

        if max_tokens is not None:
            data['max_tokens'] = max_tokens
        if top_p is not None:
            data['top_p'] = top_p
        if temperature is not None:
            data['temperature'] = temperature

        response_raw = requests.post(self.url, headers=headers, data=json.dumps(data))
        
        # Check if the request was successful
        if response_raw.status_code != 200:
            raise Exception(f"Error: {response_raw.text}")

        response_json = response_raw.json()
        content = response_json['choices'][0]['message']['content']
        # Update the history with the new message
        history.append((prompt, content))
        return content, history

if __name__ == "__main__":
    history = [('你好', '你好👋！我是人工智能助手GPT，很高兴见到你，欢迎问我任何问题。')]
    api = OpenAIAPI()
    response, updated_history = api.get_response("I didn't get it. Can you explain?", history=history)
    print(response)
    print(updated_history)
