import requests
import json

# ChatGPT API endpoint
url = 'https://api.chatanywhere.com.cn/v1/chat/completions'

# Your API key
api_key = 'sk-LxeV1tWz3ML08PBtn85cBmYu7aKXn0di6fknzxgByOOKlgrH'

# Request headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
}

# Request data
data = {
    'model': 'gpt-3.5-turbo',
    'messages': [
        {"role": "user", "content": "Hello"}
    ]
}

# Send request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Parse and print response
response_data = response.json()
print(response_data)
output = response_data['choices'][0]['message']['content']
print(output)

# Save input data as a JSON file
with open('input_data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Save output data as a JSON file
with open('output_data.json', 'w', encoding='utf-8') as file:
    json.dump(response_data, file, ensure_ascii=False, indent=4)
