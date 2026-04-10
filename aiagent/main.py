import os
from dotenv import load_dotenv
import argparse
from google.genai import types
from google import genai
from prompt import system_prompt
from functions.call_function import available_functions


def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    # get the user input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str,
                        help="The prompt to send to the model")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    # append the new message
    messages = types.Content(
        role='user', parts=[types.Part.from_text(text=args.user_prompt)])

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        )
    )

    if response.function_calls:
        for function_call in response.function_calls:
            print(
                f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)


main()
