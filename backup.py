import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="AI Agent")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the AI agent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

#response = client.models.generate_content(
    #model="gemini-2.5-flash",
    #contents=messages,
    #config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions],#temperature=0),)

usage_metadata = response.usage_metadata
function_calls = response.function_calls
function_results = []


def main():
    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0,
            ),
        )        
        if usage_metadata is None:
            raise RuntimeError("failed API request")
        
        if args.verbose:
            print("Hello from ai-agent!")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
            print(f"Response tokens: {usage_metadata.candidates_token_count}")
            print(f"Response:\n{response.text}")
            
        if function_calls:
            for function_call in function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)

                # 1. parts must exist and be non-empty
                if not function_call_result.parts:
                    raise RuntimeError("Function call returned no parts")

                part = function_call_result.parts[0]

                # 2. function_response must exist
                if part.function_response is None:
                    raise RuntimeError("Missing function_response")

                # 3. response must exist
                if part.function_response.response is None:
                    raise RuntimeError("Function response was None")

                # 4. store result
                function_results.append(part)

                # 5. verbose output
                if args.verbose:
                    print(f"-> {part.function_response.response}")
            else:
                print(f"Response:\n{response.text}")
    


if __name__ == "__main__":
    main()
