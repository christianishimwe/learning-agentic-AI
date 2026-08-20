from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
from tools import add, substract, multiply, divide


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = init_chat_model(
    "gpt-4o-mini",
    model_provider="openai",
    api_key=api_key
)

tools_for_llm = [add]

tools_for_invoking = {"add": add, "substract": substract,
                      "multiply": multiply, "divide": divide}

llm_with_tools = llm.bind_tools(tools_for_llm)

chat_history = [HumanMessage(content="what is 2 + 5")]

response_1 = llm_with_tools.invoke(chat_history)

print(response_1.tool_calls)
