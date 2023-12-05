#!/usr/bin/env python3

import openai
import os
import sys
import argparse
import json

# Color definitions
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'


# Function to manage conversation history
def manage_conversation_history(storage_file, new_entry=None, max_history=100):
    if os.path.exists(storage_file):
        with open(storage_file, 'r') as file:
            history = json.load(file)
    else:
        history = []

    if new_entry:
        history.append(new_entry)
        # Limit the history to the last 'max_history' entries
        history = history[-max_history:]
        with open(storage_file, 'w') as file:
            json.dump(history, file)

    return history

def chat_with_gpt(prompt, dry_run, new_conversation):
    storage_file = '.conversation_history.json'

    # Clear history file if new_conversation flag is True
    if new_conversation:
        history = []
        with open(storage_file, 'w') as file:
            json.dump(history, file)
    else:
        history = manage_conversation_history(storage_file)

    # Construct the messages array for the API call
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages += [{"role": "user", "content": "I am a user in MacOS Terminal running zsh in the directory /Users/dc/useful_scripts. I am interested in harnessing the power of typing in the shell, particularly in the context of Python. My goal is to become more comfortable in a command line environment and learn practical commands. Please guide me on this journey."}]
    messages += [{"role": "assistant", "content": "Within the realm of the shell's dominion, I stand ready to assist. As a denizen of MacOS Terminal, traversing the paths of zsh, thou seeketh to master the art of typing commands. Python beckons thee, and thy quest is to embrace the command line's embrace. Fear not, for I shall be thy guide in this odyssey. Let us embark on this voyage of knowledge and discovery!"}]

    # Adding previous conversation history to the messages
    for entry in history:
        user_message = {"role": "user", "content": entry["user"]}
        gpt_response = {"role": "assistant", "content": entry["gpt"]}
        messages.extend([user_message, gpt_response])

    # Adding the new user prompt to the messages
    messages.append({"role": "user", "content": prompt})

    try:
        print(f"\n\n{CYAN}#!>>> TERMINAL ADVISOR (CHATGPT): Sending for advice...\n\n{RESET}")
        print(f"{CYAN}Your query: \n{YELLOW}'{prompt}'{RESET}\n\n")

        if dry_run:
            dry_run_response = "This is a simulated (dry-run) response."
            print(f"{GREEN}Dry run mode - no API call will be made.\n\n")
            new_entry = {"user": prompt, "gpt": dry_run_response}
            manage_conversation_history(storage_file, new_entry)
            print(f"Messages history: {YELLOW}{json.dumps(messages, indent=4)}{RESET}\n\n")
            return dry_run_response

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.1
        )
        response_text = response['choices'][0]['message']['content']

        # Update conversation history if not in dry run
        if not dry_run:
            new_entry = {"user": prompt, "gpt": response_text}
            manage_conversation_history(storage_file, new_entry)

        return response_text
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    parser = argparse.ArgumentParser(description='Get GPT advice for how to use Terminal')
    parser.add_argument('prompt', type=str, help='The prompt for GPT')
    parser.add_argument('--dry-run', action='store_true', help='Run the script in dry run mode without making an API call')
    parser.add_argument('--new-conversation', action='store_true', help='Force start a new conversation')
    args = parser.parse_args()

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    openai.api_key = api_key

    response = chat_with_gpt(args.prompt, args.dry_run, args.new_conversation)
    print(f"{CYAN}#!>>> TERMINAL ADVISOR (CHATGPT): Advisor responded:{RESET}\n\n"
          f"{GREEN}{response}{RESET}"
          "\n\n====")

if __name__ == "__main__":
    main()
