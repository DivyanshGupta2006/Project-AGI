import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def scrape(url):
    try:
        print(f'Scraping URL {url}...')
        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.extract()

        content_tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'li'])

        text_lines = []
        for tag in content_tags:
            line = tag.get_text(strip=True)
            if line:
                text_lines.append(line)

        clean_text = "\n".join(text_lines)

        if len(clean_text) < 100:
            return f"Error scraping {url}: Page content blocked or unreadable."

        return clean_text[:20000]

    except Exception as e:
        return f"Error scraping {url}: {e}"