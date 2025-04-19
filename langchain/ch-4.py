# Sequential Chaining
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

model = ChatOpenAI(model="gpt-4o")

# prompt_template = ChatPromptTemplate.from_messages([
#     {"role":"system", "content":"You are a fact teller who tells fact about {animal}"},
#     {"role":"user", "content": "Tell me {fact_count} facts."}
# ])

prompt_template = ChatPromptTemplate.from_messages([
    ("system","You are a fact teller who tells fact about {animal}"),
    ("human", "Tell me {fact_count} facts.")
])

chain = prompt_template | model | StrOutputParser()

result = chain.invoke({
    "animal":"dog",
    "fact_count":"1"
})
print(result)