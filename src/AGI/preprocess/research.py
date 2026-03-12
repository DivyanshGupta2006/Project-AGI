import warnings
warnings.filterwarnings("ignore")

from AGI.preprocess import load_url, scrape_url
from AGI.utility import get_config

config = get_config.load()

def get_results(agent, prompt, summarizer_prompt):

    search_prompt = config['agent']['searching_prompt']
    scrape_prompt = config['agent']['scraping_prompt']

    search_query = agent.run(prompt=f"{search_prompt}'{prompt}'").strip()
    urls = load_url.load(search_query)

    if not urls:
        return "No research data available"

    selection_prompt = f"""
        User Goal: {prompt}

        Search Results:
        {urls}

        {scrape_prompt}
        """
    selected_urls = agent.run(selection_prompt).strip()

    if "NONE" in selected_urls or "http" not in selected_urls:
        return "No research data available"

    best_urls = [url.strip() for url in selected_urls.split(',') if "http" in url]

    compiled_research = []
    successful_scrapes = 0

    for url in best_urls:
        if successful_scrapes >= 3:
            break

        try:
            content = scrape_url.scrape(url)
            compiled_research.append(f"Source: {url}\nContent:\n{content}\n")
            successful_scrapes += 1
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            continue

    if not compiled_research:
        return "Research failed: Could not scrape any of the selected sources."

    print("Synthesizing scraped data...")
    raw_data_string = "\n".join(compiled_research)

    final_synthesis_prompt = f"""{summarizer_prompt.replace('{user_prompt}', prompt).replace('{compiled_research}', raw_data_string)}"""

    return agent.run(final_synthesis_prompt)
