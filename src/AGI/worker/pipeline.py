import time
from AGI.worker.agent import Agent


def run(model,
        api_key,
        prompt,
        actor_prompt,
        critic_prompt,
        system_prompt,
        instructions,
        upload_dir):
    actor = Agent(model, api_key, system_prompt, actor_prompt, instructions)
    critic = Agent(model, api_key, system_prompt, critic_prompt, instructions)
    actor_out = actor.run(prompt, media=upload_dir)
    print("Buffer time...")
    time.sleep(60)
    critic_out = critic.run("", f"Prompt: \n{prompt} \nActor Response: \n{actor_out}", media=upload_dir)
    print("Please wait...")
    time.sleep(60)
    return actor.run(prompt, f"Prompt: \n{prompt} \nInitial Actor Response: \n{actor_out} \nCritic Response: \n{critic_out}", media=upload_dir)