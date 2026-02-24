from AGI.worker.agent import Agent
from AGI.preprocess import research

def run(model,
        key_manager,
        prompt,
        actor_prompt,
        critic_prompt,
        researcher_prompt,
        system_prompt,
        instructions,
        upload_dir,
        enable_web=True):
    actor = Agent(model, key_manager, system_prompt, actor_prompt, instructions)
    critic = Agent(model, key_manager, system_prompt, critic_prompt, instructions)
    web_context = 'No Context Available'
    if enable_web:
        researcher = Agent(model, key_manager, system_prompt, researcher_prompt, instructions)
        web_context = research.get_results(researcher, prompt)
    print("Getting preliminary actor's output...")
    actor_out = actor.run(prompt,
                          context=f"Research data: \n{web_context}",
                          media=upload_dir)
    print("Getting critic's judgement...")
    critic_out = critic.run("",
                            context=f"Prompt: \n{prompt} \nResearch data: \n{web_context} \nActor Response: \n{actor_out}",
                            media=upload_dir)
    print("Enforcing critic's judgement...")
    return actor.run(prompt,
                     context=f"Prompt: \n{prompt} \nResearch data: \n{web_context} \nInitial Actor Response: \n{actor_out} \nCritic Response: \n{critic_out}",
                     media=upload_dir)