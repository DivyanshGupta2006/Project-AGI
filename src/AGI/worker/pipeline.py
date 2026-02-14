from AGI.worker.agent import Agent


def run(model,
        api_key,
        prompt,
        actor_prompt,
        critic_prompt,
        system_prompt):
    actor = Agent(model, api_key)
    critic = Agent(model, api_key)
    actor_out = actor.run(prompt, actor_prompt, system_prompt)
    critic_out = critic.run(f'Prompt: {prompt} \nInitial Response: {actor_out}', critic_prompt, system_prompt)
    return actor.run(f'Prompt: {prompt} \nInitial Response: {actor_out} \nCritic Response: {critic_out}', actor_prompt, system_prompt)