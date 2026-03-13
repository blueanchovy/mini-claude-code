import os, argparse, re, time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt_v3
from functions.genai.call_function import available_functions, call_function



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    system_prompt = system_prompt_v3

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    #keeps a log of each action performed
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if not api_key:
            raise RuntimeError("Api Key not found!")
    
    #to limit tool calls and burning through tokens
    max_iterations = 20
    iteration = 0

    while iteration < max_iterations:
        #try catch to subbvert 5RPM limit in gemini api
        try:
            response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0),
        )
        except Exception as e:
            if "429" in str(e):
                match = re.search(r'retryDelay.*?(\d+)s', str(e))
                wait = int(match.group(1)) + 5 if match else 60
                print(f"Rate limit hit, waiting {wait} seconds...")
                time.sleep(wait)
                continue
            raise
        iteration += 1

        candidates = response.candidates

        if candidates:
            for candidate in candidates:
                messages.append(candidate.content)

        if(response.usage_metadata == None): 
            raise RuntimeError("Could not find usage metadata in llm gemini response!")
        
        candidates_token_count, prompt_token_count = response.usage_metadata.candidates_token_count, response.usage_metadata.prompt_token_count
        if(args.verbose == True):
            print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}")

        function_results = []
        if response.function_calls != None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)

                if len(function_call_result.parts) == 0:
                    raise Exception
                
                if function_call_result.parts[0].function_response == None:
                    raise Exception
                
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception
                
                function_results.append(function_call_result.parts[0])
                
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                print(f"Calling function: {function_call.name}({function_call.args})")

            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            break
    else:
        # for loop exhausted without breaking
        print(f"Agent did not produce a final response within {max_iterations} iterations.")
        exit(1)
    
if __name__ == "__main__":
    main()
