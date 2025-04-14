from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# response = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         {"role": "user", "content":"what is 2 + 2 * 0"}
#     ]
# )
# print(response.choices[0].message.content)

response = client.responses.create(
    model='gpt-4',
    input="what is 2 + 4"
)

print(response.output_text)