import warnings
warnings.filterwarnings("ignore")

from AGI.preprocess import load_url, scrape_url
from AGI.utility import get_config

config = get_config.load()

def get_results(agent, prompt):

    search_prompt = config['agent']['searching_prompt']
    scrape_prompt = config['agent']['scraping_prompt']

    search_query = agent.run(
        prompt=f"{search_prompt}'{prompt}'"
    ).strip()

    urls = load_url.load(search_query)
    if not urls:
        return "No research data available"

    selection_prompt = f"""
        User Goal: {prompt}

        Search Results:
        {urls}

        {scrape_prompt}
        """
    best_url = agent.run(selection_prompt).strip()

    if "NONE" in best_url or "http" not in best_url:
        return "No research data available"

    content = scrape_url.scrape(best_url)
    return f"Source: {best_url}\n\nContent:\n{content}"