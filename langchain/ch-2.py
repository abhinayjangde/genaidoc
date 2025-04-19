from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Chaining example : https://python.langchain.com/docs/integrations/chat/openai/

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}.",
        ),
        ("human", "{input}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o")

chain = prompt | llm

response = chain.invoke({
    "input_language":"English",
    "output_language":"German",
    "input":"I love programming."
})

print(response)
print(response.content) # Ich liebe Programmieren.