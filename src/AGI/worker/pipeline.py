from AGI.worker.agent import Agent


def run(model,
        key_manager,
        prompt,
        actor_prompt,
        critic_prompt,
        system_prompt,
        instructions,
        upload_dir):
    actor = Agent(model, key_manager, system_prompt, actor_prompt, instructions)
    critic = Agent(model, key_manager, system_prompt, critic_prompt, instructions)
    actor_out = actor.run(prompt, media=upload_dir)
    critic_out = critic.run("", f"Prompt: \n{prompt} \nActor Response: \n{actor_out}", media=upload_dir)
    return actor.run(prompt, f"Prompt: \n{prompt} \nInitial Actor Response: \n{actor_out} \nCritic Response: \n{critic_out}", media=upload_dir)