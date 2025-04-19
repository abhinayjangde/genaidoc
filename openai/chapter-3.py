from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role":"system", "context":"You an helpful ai assistant and your name is Jarvis."},
        {"role":"user", "context": "what is your name ?"}
    ]
)

print(response.choices[0].message.content)