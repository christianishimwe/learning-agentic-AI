from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@tool
def substract(a: int, b: int) -> int:
    """substract b from a"""
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


@tool
def divide(a: int, b: int) -> float:
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
