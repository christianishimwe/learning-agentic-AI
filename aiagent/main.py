import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types


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
        model='gemini-2.5-flash', contents=messages)

    print(response.text)
    if response is None or response.usage_metadata is None:
        print("response is malformed")
        return
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
