import os
import sys
import time
import re
from dotenv import load_dotenv

from AGI.worker import pipeline
from AGI.utility import get_path, get_config, read_file


load_dotenv()
config = get_config.load()

def start():
    print("Welcome to AGI!")
    """
    Algorithm - 1
    Feed the prompt to a single instance of agent and return response
    """
    # input prompt
    prompt = read_file.read_prompt()
    choice = input('Enter chat name to continue (or enter new to create a new chat): ')
    chats = []
    path = get_path.absolute(config['paths']['chats_metadata'])
    chat_dir = get_path.absolute(config['paths']['chats'])
    upload_dir = get_path.absolute(config['paths']['uploads'])
    get_path.check(chat_dir)
    get_path.check(upload_dir)
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            chats.append(line.strip())

    if choice == 'new':
        name = input('Enter new chat name: ')
        if name in chats:
            print('Chat already exists!')
            sys.exit(0)
        else:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(name + '\n')
            upload_dir = upload_dir / name
            get_path.check(upload_dir)
            path = get_path.absolute(f'{chat_dir}/{name}.md')
    elif choice in chats:
        upload_dir = upload_dir / choice
        path = get_path.absolute(f'{chat_dir}/{choice}.md')
    else:
        print('Invalid chat name!')
        sys.exit(0)
    print('Upload files (if any)')
    _ = input('Press enter to continue...')
    print("Generating...")

    # output response
    model = config['agent']['model']
    api_key = os.getenv("API_KEY")
    actor_prompt = config["agent"]["actor_prompt"]
    critic_prompt = config["agent"]["critic_prompt"]
    system_prompt = config["agent"]["system_prompt"]
    instructions = config["agent"]["instructions"]
    start_time = time.perf_counter()

    try:
        response = pipeline.run(model, api_key, prompt, actor_prompt, critic_prompt, system_prompt, instructions, upload_dir)
        with open(chat_dir / path, 'a', encoding="utf-8") as f:
            f.write(f'# Prompt: \n{prompt} \n\n# Response: \n{response}\n___\n')
    except Exception as e:
        msg = e.message

        model_match = re.search(r"model:\s*([^\s\n]+)", msg)
        model_name = model_match.group(1) if model_match else None

        retry_match = re.search(r"Please retry in\s*([\d\.]+s)", msg)
        retry_time = retry_match.group(1) if retry_match else None

        print(f"Model: {model_name}")
        print(f"Retry Time: {retry_time}")

    end_time = time.perf_counter()

    print(f"Time taken: {(end_time - start_time):.2f} seconds")
    print("Thank you for using AGI!")