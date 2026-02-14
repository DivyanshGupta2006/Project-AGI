import os
from dotenv import load_dotenv

from AGI.worker.agent import Agent
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

    # instantiate agent
    model = config['agent']['model']
    api_key = os.getenv("API_KEY")
    agent = Agent(model, api_key)

    # output response
    system_prompt = config["agent"]["system_prompt"]
    response = agent.run(prompt, system_prompt)
    path = get_path.absolute(config['paths']['response'])
    with open(path, 'w', encoding="utf-8") as f:
        f.write(f'Prompt: {prompt} \n\nResponse: {response}')

    print("Thank you for using AGI!")