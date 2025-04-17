from fastapi import FastAPI
from ollama import Client
from fastapi import Body

app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

client.pull("deepseek-r1:1.5b") # ollama run deepseek-r1:1.5b

@app.post('/chat')
def chat(message:str=Body(...,description="Chat Message")):
    response = client.chat(
        model="deepseek-r1:1.5b",
        messages=[
            {"role":"user", "content":message}
        ]
    )
    return response.message.content