from langsmith import traceable
import dotenv

from AGI.preprocess import research
from AGI.worker.agent import Agent

dotenv.load_dotenv()

@traceable(run_type="tool", name="Web Research")
def run_researcher(researcher, prompt, summarizer_prompt):
    return research.get_results(researcher, prompt, summarizer_prompt)


@traceable(run_type="llm", name="Actor (Draft)")
def run_actor_draft(actor, prompt, context, media):
    return actor.run(prompt, context=context, media=media)


@traceable(run_type="llm", name="Critic (Review)")
def run_critic(critic, prompt, context, media):
    return critic.run(prompt, context=context, media=media)


@traceable(run_type="llm", name="Actor (Final Output)")
def run_actor_final(actor, prompt, context, media):
    return actor.run(prompt, context=context, media=media)


@traceable(run_type="chain", name="Multi-Agent Execution")
def run(model,
        key_manager,
        personality,
        prompt,
        summary,
        last_interaction,
        actor_prompt,
        critic_prompt,
        researcher_prompt,
        summarizer_prompt,
        system_prompt,
        instructions,
        upload_dir,
        enable_web=True):

    actor_system_prompt = f"""
    {system_prompt}
    
    CRITICAL INSTRUCTION: Adopt the following persona/tone for all outputs: {personality}
    """
    critic_system_prompt = f"""{system_prompt}
    
    CRITICAL INSTRUCTION: The Actor you are reviewing has been instructed to write in the following persona: {personality}.
    Do NOT penalize stylistic choices related to this persona. Focus your critique on logic, factual accuracy, and prompt adherence."""

    actor = Agent(model, key_manager, actor_system_prompt, actor_prompt, instructions)
    critic = Agent(model, key_manager, critic_system_prompt, critic_prompt, instructions)

    chat_history_context = f"""
    === CHAT HISTORY CONTEXT ===
    Running Summary: {summary if summary else 'None'}
    Last Interaction: {last_interaction if last_interaction else 'None'}
    ============================
    """

    web_context = 'No Context Available'
    if enable_web:
        researcher = Agent(model, key_manager, system_prompt, researcher_prompt, instructions)
        web_context = run_researcher(researcher, f"{prompt}\n\n{chat_history_context}", f"{summarizer_prompt}")

    print("Getting preliminary actor's output...")
    actor_context = f"Research data: \n{web_context}\n\n{chat_history_context}"
    actor_out = run_actor_draft(actor, prompt, context=actor_context, media=upload_dir)

    print("Getting critic's judgement...")
    critic_context = f"Prompt: \n{prompt} \nResearch data: \n{web_context}\n\n{chat_history_context} \nActor Response: \n{actor_out}"
    critic_out = run_critic(critic, "", context=critic_context, media=upload_dir)

    print("Enforcing critic's judgement...")
    final_context = f"Prompt: \n{prompt} \nResearch data: \n{web_context}\n\n{chat_history_context} \nInitial Actor Response: \n{actor_out} \nCritic Response: \n{critic_out}"
    return run_actor_final(actor, prompt, context=final_context, media=upload_dir)