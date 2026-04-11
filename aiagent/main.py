import os
from dotenv import load_dotenv
import argparse
from google.genai import types
from google import genai
from prompt import system_prompt
from functions.call_function import available_functions, call_function


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
            # print(
            #    f"Calling function: {function_call.name}({function_call.args})")
            function_call_response = call_function(
                function_call, verbose=args.verbose)
            # if the function_call_response object has an empty parts list, we will print an error message
            if not function_call_response.parts:
                print(
                    f"Error: function {function_call.name} returned an empty response"
                )
            # if the first part of the function_call_response has an empty response, we will print an error message
            if not function_call_response.parts[0]:
                print(
                    f"Error: function {function_call.name} returned an empty response"
                )
            if not function_call_response.parts[0].function_response:
                print(
                    f"Error: function {function_call.name} returned an empty response"
                )
            if not function_call_response.parts[0].function_response.response:
                print(
                    f"Error: function {function_call.name} returned an empty response"
                )
            # whew, that was a lot of checks, now we can safely print the response
            # now we know that the function returned some response
            # TO DO HERE!!! comint up later

            if args.verbose:
                print(
                    f"Function {function_call.name} returned response: {function_call_response.parts[0].function_response.response}"
                )
    else:
        print(response.text)


main()
