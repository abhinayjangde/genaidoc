from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


system_prompt="""
You are an helpful AI assistant and your name is Codebhaiya. Your task to help coding related problems of the user.

Example:

Input: How to write a adding program in python.
Output: 
def add(a,b):
    return a + b



"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role":"system",
            "content": system_prompt
        },
        {
            "role":"user",
            "content":"What is your name ?"
        }
    ]
)

print(response.choices[0].message.content)