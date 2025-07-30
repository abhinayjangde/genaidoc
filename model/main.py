import requests

url = "http://localhost:12434/engines/llama.cpp/v1/chat/completions"

data = {

   "model":"ai/smollm2:latest",
   "messages":[
     {
        "role":"system",
        "content":"You are an helpful AI assistant"
    },
    {
        "role":"user",
        "content": "what 2 + 4 ?"
    }
   ]
}

response = requests.post(url, json=data)

response.raise_for_status()

print(response.json()["choices"][0]["message"]["content"])

