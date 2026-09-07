import random
import string
from typing import TypedDict
from langgraph.graph import StateGraph, END


class ChainState(TypedDict):
    n: int
    letter: str


initial_state = ChainState(n=1, letter='a')
print(initial_state)


def add(state: ChainState) -> ChainState:
    random_letter = random.choice(string.ascii_lowercase)
    return {**state, "n": state["n"] + 1, "letter": random_letter}


def printout(state: ChainState) -> ChainState:
    print(f"Current n: {state["n"]} and current letter: {state["letter"]}")
    return state


def stop_condition(state: ChainState) -> bool:
    return state["n"] >= 13


workflow = StateGraph(ChainState)
workflow.add_node("add", add)
workflow.add_node("print", printout)
workflow.add_edge("add", "print")
workflow.add_conditional_edges(
    "print",
    stop_condition,
    {
        True: END,
        False: "add"
    }
)
workflow.set_entry_point("add")
app = workflow.compile()

result = app.invoke({"n": 1, "letter": "a"})
print(result)
