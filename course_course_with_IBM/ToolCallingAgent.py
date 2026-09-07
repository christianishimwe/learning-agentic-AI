from langchain_core.messages import HumanMessage, ToolMessage, BaseMessage


class ToolCallingAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.tools_map = {tool.name: tool for tool in tools}
        self.llm_with_tools = llm.bind_tools(tools)

    def run(self, query):
        chat_history: list[BaseMessage] = [HumanMessage(content=query)]

        response_1 = self.llm_with_tools.invoke(chat_history)
        chat_history.append(response_1)
        tool_calls_1 = response_1.tool_calls
        tool_1_name = tool_calls_1[0]["name"]
        tool_1_args = tool_calls_1[0]["args"]
        tool_call_1_id = tool_calls_1[0]["id"]
        tool_response = self.tools_map[tool_1_name].invoke(tool_1_args)
        tool_message = ToolMessage(
            content=tool_response, tool_call_id=tool_call_1_id)
        chat_history.append(tool_message)

        # pass the updated chat history to the llm
        answer = self.llm_with_tools.invoke(chat_history)
        return answer.content
