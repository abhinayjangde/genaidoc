from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

config = {
    "version":"v1.1",
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QDRANT_HOST,
            "port": 6333
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4o"
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-large"
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URL,
            "username": NEO4J_USERNAME,
            "password":NEO4J_PASSWORD
        }
    }
}

mem_client = Memory.from_config(config)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def chat(message):

    mem_result = mem_client.search(query=message, user_id="abhi")

    memories ="\n".join(m["memory"] for m in mem_result["results"])
  
    print(f"\n\nMEMORY:\n\n{memories}\n\n")

    SYSTEM_PROMPT=f"""
        You are a Memory-Aware Fact Extraction Agent, an advanced AI designed to
        systematically analyze input content, extract structured knowledge, and maintain an
        optimized memory store. Your primary function is information distillation
        and knowledge preservation with contextual awareness.

        Tone: Professional analytical, precision-focused, with clear uncertainty signaling
        
        Memory:
        {memories}
    """

    messages = [
        { "role": "system", "content": SYSTEM_PROMPT },
        {"role":"user", "content": message}
    ]

    result = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    messages.append(
        {"role":"assistant", "content": result.choices[0].message.content}
    )   

    mem_client.add(messages, user_id="abhi")

    return result.choices[0].message.content


while True:
    message = input("👤> ")
    if message == "bye":
        break
    res = chat(message=message)
    print("🤖> ", res)


