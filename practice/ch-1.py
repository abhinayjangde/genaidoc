from openai import OpenAI


client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    input="What is the size of this list in python l=[1,2,4]",
    stream=True
)
for event in response:
    print(event)