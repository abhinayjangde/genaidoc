from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

pdf_path = Path(__file__).parent / "Patent.pdf"
# print(pdf_path)

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load() # python list
# print(docs[1].metadata['total_pages'])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

split_docs = text_splitter.split_documents(documents=docs)

# print("Informations")
# print("DOCS: ",len(docs))
# print("SPLIT: ", len(split_docs))

embedder = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=os.getenv("OPENAI_API_KEY")
)

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     collection_name="leaning_langchain",
#     url="http://localhost:6333",
#     embedding=embedder
# )

# vector_store.add_documents(split_docs)
print("injection done")

retriver = QdrantVectorStore.from_existing_collection(
    collection_name="leaning_langchain",
    url="http://localhost:6333",
    embedding=embedder
)

relevant_chunks = retriver.similarity_search(
    query="what is product patent ?"
)
# print(relevant_chunks)

SYSTEM_PROMPT=f"""

You are an helpful AI Assistant who responds based on the available context.

Context:
{relevant_chunks}

"""


