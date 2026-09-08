

# the Right credentials
from typing import TypedDict
from langgraph.graph import StateGraph, END


true_credentials = {
    "username": "test_user",
    "password": "secure_password",
}

# create the state


class CredentialsState(TypedDict):
    username: str
    password: str
    is_aunthenticated: bool

# the input node


def input_node(state: CredentialsState) -> CredentialsState:
    # ask the user's username
    new_username = input("Enter your username:")
    # ask the user's password
    new_password = input("Enter your password:")

    return {**state, "username": new_username, "password": new_password}


def validate_credential(state: CredentialsState) -> CredentialsState:
    # check if the credentials are correct
    if state["username"] == true_credentials["username"] and state["password"] == true_credentials["password"]:
        return {**state, "is_aunthenticated": True}
    else:
        return {**state, "is_aunthenticated": False}


def success(state: CredentialsState) -> CredentialsState:
    print("Login successful!")
    return state


def failure(state: CredentialsState) -> CredentialsState:
    print("Login failed. Please try again.")
    return state


def check_authentication(state: CredentialsState) -> str:
    if state["is_aunthenticated"]:
        return "success"
    else:
        return "failure"


workflow = StateGraph(CredentialsState)
workflow.add_node("input", input_node)
workflow.add_node("validate", validate_credential)
workflow.add_node("success", success)
workflow.add_node("failure", failure)

workflow.add_edge("input", "validate")
workflow.add_conditional_edges(
    "validate",
    check_authentication,
    {
        "success": "success",
        "failure": "failure"
    }
)
workflow.add_edge("success", END)
workflow.add_edge("failure", "input")
workflow.set_entry_point("input")

app = workflow.compile()

app.invoke({"username": "", "password": "", "is_aunthenticated": False})
