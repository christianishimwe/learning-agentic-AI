from tools import add, substract, multiply, divide
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from ToolCallingAgent import ToolCallingAgent

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = init_chat_model(
    "gpt-4o-mini",
    model_provider="openai",
    api_key=api_key
)

tools_for_llm = [add, substract, divide, multiply]

tools_map = {"add": add, "substract": substract,
             "multiply": multiply, "divide": divide}

agent_1 = ToolCallingAgent(llm, tools_for_llm)
print(agent_1.run("what is 3 minus 2"))
