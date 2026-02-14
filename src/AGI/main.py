import os
import time
from dotenv import load_dotenv

from AGI.worker import pipeline
from AGI.utility import get_path, get_config


load_dotenv()
config = get_config.load()

def start():
    print("Welcome to AGI!")
    """
    Algorithm - 1
    Feed the prompt to a single instance of agent and return response
    """
    # input prompt
    prompt = input("Enter Prompt: ")
    print("Generating...")

    # output response
    model = config['agent']['model']
    api_key = os.getenv("API_KEY")
    actor_prompt = config["agent"]["actor_prompt"]
    critic_prompt = config["agent"]["critic_prompt"]
    system_prompt = config["agent"]["system_prompt"]
    instructions = config["agent"]["instructions"]
    start_time = time.perf_counter()
    response = pipeline.run(model, api_key, prompt, actor_prompt, critic_prompt, system_prompt, instructions)
    path = get_path.absolute(config['paths']['response'])
    with open(path, 'w', encoding="utf-8") as f:
        f.write(f'Prompt: \n{prompt} \n\nResponse: \n{response}')
    end_time = time.perf_counter()

    print(f"Time taken: {(end_time - start_time):.2f} seconds")
    print("Thank you for using AGI!")