import os
import argparse
from google import genai
from dotenv import load_dotenv
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    for _ in range(20):
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            if response.usage_metadata != None: 
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if not response.function_calls:
            print(response.text)
            break
        else:
            messages.append(response.candidates[0].content)
            for function_call in response.function_calls:
                result_message = call_function(function_call, args.verbose)
                if result_message['content']:
                    function_response_part = types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": result_message['content']},
                    )
                    messages.append(types.Content(role="tool", parts=[function_response_part]))
                    if args.verbose == True:
                        print(f"-> {result_message['content']}")
                else:
                    raise Exception("content is empty")
    else:
        print("agent didn't produce a final response after 20 iterations")
        sys.exit(1)

if __name__ == "__main__":
    main()
