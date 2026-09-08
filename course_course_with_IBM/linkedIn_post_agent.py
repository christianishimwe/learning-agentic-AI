
import os
from typing import Sequence, List
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import MessageGraph
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = init_chat_model(
    "gpt-4o-mini",
    model_provider="openai",
    api_key=api_key
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional LinkedInContent assistant tasked with crafting"
            "engaging,insightful and well structured linkedIn posts."
            "Generate the best linkedInpost possible for the user's requests"
            "if the user provides feedback or critique, respond with a refined version of "
            "your previous attempts, imporving clarity tone or engagement as needed"
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generate_chain = generation_prompt | llm


# now let's create a chain for the reflection llm
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
        You are a professional LinkedIn content strategist tasked with
        and thoruhg leadership expert. your task is to critically evaluate the given linked in post
        and provide a comprehension ciritique.
        follow the following guidelines when providing feedback:
        - Evaluate the clarity of the post. Is the message clear and easy to understand?
        - mention specific areas where the post could be improved for clarity.
        = suggest actionable improvements to enhance the clarity of the post.

        your critique will be used to improve the post in the next revision step
        so ensure your feedback is thoughtful, constructive and practical
        """
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)
reflection_chain = reflection_prompt | llm

graph = MessageGraph()


def generation_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
    # generate the linkedInPost
    generated_post = generate_chain.invoke({"messages": state})
    return [AIMessage(content=generated_post.content)]


def reflection_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
    # reflect on the linkedInPost
    critique = reflection_chain.invoke({"messages": state})
    return [HumanMessage(content=critique.content)]
