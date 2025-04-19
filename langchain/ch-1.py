from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

result = llm.invoke("what is 2+2 ?")
print(result.content)