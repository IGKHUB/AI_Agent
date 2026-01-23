import os
import argparse
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="AI Agent")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the AI agent")
args = parser.parse_args()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=args.user_prompt,
)
usage_metadata = response.usage_metadata

def main():
    if usage_metadata is not None:
        print("Hello from ai-agent!")
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")
        print(f"Response:\n{response.text}")
    else:
        raise RuntimeError("failed API request")


if __name__ == "__main__":
    main()
