import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

if api_key == None:
    raise Exception("API key not found, check .env GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from aiagent!")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


    for _ in range(20):

        response = client.models.generate_content(model="gemini-2.5-flash", 
                                                contents=messages, 
                                                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)

        if response.usage_metadata == None:
            raise RuntimeError("Failed to receive a valid response from API")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates != None:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if response.function_calls != None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)

                if function_call_result.parts == None:
                    raise Exception("Empty function_call_result.parts")
                
                if function_call_result.parts[0].function_response == None:
                    raise Exception("Invalid function_response")
                
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Invalid response")
                
                function_results = []
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                messages.append(types.Content(role="user", parts=function_results))
                # print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(response.text)
            break
        
    if response.text == None:
        print("Agent reached max interations without returning a response")
        exit(1)
        

if __name__ == "__main__":
    main()


# uv run main.py [PROMPT]