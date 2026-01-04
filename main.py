import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    print("Hello from mini-claude-code!")

    if(api_key):
        print("Api Key found")
    else: 
        raise RuntimeError("Api Key not found!")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents= messages
    )

    if(response.usage_metadata == None): 
        raise RuntimeError("Could not find usage metadata in llm gemini response!")
    
    candidates_token_count, prompt_token_count = response.usage_metadata.candidates_token_count, response.usage_metadata.prompt_token_count
    if(args.verbose == True):
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}")
    print(response.text)
if __name__ == "__main__":
    main()
