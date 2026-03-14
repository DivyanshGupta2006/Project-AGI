from langsmith import traceable

from AGI.worker.agent import Agent
from AGI.utility import read_file

@traceable(run_type="llm", name="Summarizer (Memory Update)")
def update(model, key_manager, chat, system_prompt, summary_prompt, instructions, summary_path):
    summary = read_file.read_summary(chat)
    last_interaction = read_file.read_last_interaction(chat)
    print("Updating Summary...")

    summarizer_system_prompt = f"""{system_prompt}

    CRITICAL INSTRUCTION: You are a memory manager.
    Your only job is to update conversation summaries accurately and concisely without adding external fluff."""
    summary_prompt = summary_prompt.replace("{old_summary}", summary).replace("{interaction}", last_interaction)
    summarizer = Agent(model, key_manager, summarizer_system_prompt, summary_prompt, instructions)

    new_summary = summarizer.run("Summarize the given chat history effectively so that it can be passed as context to other LLMs")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(new_summary)

    return new_summary