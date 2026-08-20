from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage, BaseMessage
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

tools_map = {"add": add, "substract": substract,
             "multiply": multiply, "divide": divide}

llm_with_tools = llm.bind_tools(tools_for_llm)

chat_history: list[BaseMessage] = [HumanMessage(content="what is 2 + 5")]

response_1 = llm_with_tools.invoke(chat_history)
chat_history.append(response_1)
tool_calls_1 = response_1.tool_calls
tool_1_name = tool_calls_1[0]["name"]
tool_1_args = tool_calls_1[0]["args"]
tool_call_1_id = tool_calls_1[0]["id"]
tool_response = tools_map[tool_1_name].invoke(tool_1_args)
tool_message = ToolMessage(content=tool_response, tool_call_id=tool_call_1_id)
chat_history.append(tool_message)

# pass the updated chat history to the llm
answer = llm_with_tools.invoke(chat_history)
print(answer)
