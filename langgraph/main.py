from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from pydantic import BaseModel
import os


load_dotenv()
client = wrap_openai(OpenAI())

print(os.getenv("OPENAI_API_KEY"))
# Schema
class DetectCallResponse(BaseModel):
    is_question_ai: bool

class State(TypedDict):
    user_message: str
    ai_message: str
    is_coding_question: bool

def detect_query(state: State):
    user_message = state.get("user_message")

    SYSTEM_PROMPT="""
    You are an AI assistant. Your job is to detect if the user's query is related to coding question or not.
    Return the response in specified JSON boolean only.
    """
    # OpenAI Call
    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=DetectCallResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )

    print(result.choices[0].message.parsed)
    state["is_coding_question"] = True
    return state

def route_edge(state: State) -> Literal["solve_coding_question", "solve_simple_question"]:
    is_coding_question = state.get("is_coding_question")

    if is_coding_question :
        return "solve_coding_question"
    else:
        return "solve_simple_question"

def solve_coding_question(state:State):
    user_message = state.get("user_message")

    # Call OpenAI (TO solve coding question gpt-4.1)
    state["ai_message"] = "Here is solution of your coding question: "
    return state

def solve_simple_question(state:State):
    user_message = state.get("user_message")

    # Call OpenAI (To solve non coding question use small llm (gpt-4o-mini)
    state["ai_message"] = "Please ask some coding related question: "
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)
graph_builder.add_node("route_edge", route_edge)

graph_builder.add_edge(START, "detect_query")
graph_builder.add_conditional_edges("detect_query", route_edge)

graph_builder.add_edge("solve_coding_question",END)
graph_builder.add_edge("solve_simple_question",END)

graph = graph_builder.compile()

# Use graph

def call_graph():
    state = {
        "user_message": "Hey there, how are you ?",
        "ai_message": "",
        "is_coding_question" : False
    }
    result = graph.invoke(state)
    print("Final result ", result)

call_graph()