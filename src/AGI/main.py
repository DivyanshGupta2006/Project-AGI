import sys
import time

from dotenv import load_dotenv

from AGI.utility import get_path, get_config, read_file, key_manager
from AGI.worker import pipeline

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
    chats = []
    path = get_path.absolute(config['paths']['chats_metadata'])
    chat_dir = get_path.absolute(config['paths']['chats'])
    upload_dir = get_path.absolute(config['paths']['uploads'])
    get_path.check(path.parent)
    get_path.check(chat_dir)
    get_path.check(upload_dir)
    try:
        with open(path, 'w') as file:
            file.write("")
    except FileExistsError:
        pass
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            chats.append(line.strip())

    choice = input('Enter chat name to continue (or enter new to create a new chat): ')

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
    key = key_manager.Key()
    actor_prompt = config["agent"]["actor_prompt"]
    critic_prompt = config["agent"]["critic_prompt"]
    researcher_prompt = config["agent"]["researcher_prompt"]
    system_prompt = config["agent"]["system_prompt"]
    instructions = config["agent"]["instructions"]
    start_time = time.perf_counter()

    response = pipeline.run(model, key, prompt, actor_prompt, critic_prompt, researcher_prompt, system_prompt, instructions, upload_dir)
    with open(chat_dir / path, 'a', encoding="utf-8") as f:
        f.write(f'# Prompt: \n{prompt} \n\n___\n# Response: \n{response}\n___\n')

    end_time = time.perf_counter()

    print(f"Time taken: {(end_time - start_time):.2f} seconds")
    print("Thank you for using AGI!")