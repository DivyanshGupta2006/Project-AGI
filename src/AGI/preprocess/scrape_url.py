import requests
from bs4 import BeautifulSoup


def scrape_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator='\n')

        clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        return clean_text[:20000]
    except Exception as e:
        return f"Error scraping {url}: {e}"