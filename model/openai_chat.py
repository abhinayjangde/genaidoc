from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key="anything", base_url="http://localhost:12434/engines/llama.cpp/v1")

prompt = "how are you ?"

messages = [
    {
        "role":"user",
        "content":prompt
    }
]

response = client.chat.completions.create(
    model= os.getenv("MODEL"),
    messages= messages
)

print(response.choices[0].message.content)