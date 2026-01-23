import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="AI Agent")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the AI agent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
)
usage_metadata = response.usage_metadata


def main():
    if usage_metadata is not None:
        if args.verbose:
            print("Hello from ai-agent!")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
            print(f"Response tokens: {usage_metadata.candidates_token_count}")
            print(f"Response:\n{response.text}")
        else:
            print(f"Response:\n{response.text}")
    else:
        raise RuntimeError("failed API request")


if __name__ == "__main__":
    main()
