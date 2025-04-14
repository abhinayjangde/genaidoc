from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role":"system",
            "content":"You are an helpful AI assistant and your name is Codebhaiya."
        },
        {
            "role":"user",
            "content":"What is your name ?"
        }
    ]
)

print(response.choices[0].message.content)