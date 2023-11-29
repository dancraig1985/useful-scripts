#!/usr/bin/env python3

import openai
import os
import sys
import argparse

# Color definitions
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

def chat_with_gpt(prompt, dry_run):
    try:
        current_working_directory = os.getcwd()
        preamble = (f"I am a user in MacOS Terminal running zsh in the directory "
                    f"{current_working_directory}. I like to write python and am "
                    "learning how to feel more comfortable in a command line environment. "
                    "If I am asking a simple question please don't feel the need to add explanation. "
                    "Often I will just be asking for simple examples of practical commands to complete a task."
                    "If I want you to expand with a long example I will ask questions that are more open-ended "
                    "or otherwise specifying that I want you to go more in depth. Basically I don't have "
                    "unlimited tokens and would rather conserve them for simple questions with the option. "
                    "to spend tokens when I ask for it. I will be interacting with you via a script in my Terminal. "
                    "Feel free to make brief playful references to the interesting setting in which we meet."
                    "Now, teach me the power of typing in the shell! And more specifically, please answer "
                    "the following query to the best of your ability: ")

        print(f"\n\n{CYAN}#!>>> TERMINAL ADVISOR (CHATGPT): Sending for advice...\n\n{RESET}")
        print(f"{CYAN}Your query: \n{YELLOW}'{prompt}'{RESET}\n\n")
        
        if dry_run:
            print(f"{GREEN}Dry run mode - no API call will be made.\n\n")
            print("Intended API request details:\n")
            print(f"Full Prompt: {YELLOW}{preamble}{prompt}{RESET}\n\n")
            # You can add more details here if needed
            return "This is a simulated (dry-run) response."

        response = openai.Completion.create(
            engine="text-davinci-003",  # Adjust the engine if needed
            prompt=f"{preamble}{prompt}",
            max_tokens=2500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    parser = argparse.ArgumentParser(description='Get GPT advice for how to use Terminal')
    parser.add_argument('prompt', type=str, help='The prompt for GPT')
    parser.add_argument('--dry-run', action='store_true', help='Run the script in dry run mode without making an API call')
    args = parser.parse_args()

    # Ensure the API key is set
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    # Set the API key
    openai.api_key = api_key

    # Get the response from GPT
    response = chat_with_gpt(args.prompt, args.dry_run)
    print(f"{CYAN}#!>>> TERMINAL ADVISOR (CHATGPT): Advisor responded:{RESET}\n\n"
        f"{GREEN}{response}{RESET}"
        "\n\n====")

if __name__ == "__main__":
    main()
