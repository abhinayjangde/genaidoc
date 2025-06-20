from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# response
"""
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Hi"
        }
    ]
)

print(response.choices[0].message.content, end="")
"""

# List Models

'''
models = client.models.list()
for model in models:
    print(model.id)
'''

# Streaming
'''
response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content)
'''