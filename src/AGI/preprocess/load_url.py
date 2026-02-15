from googlesearch import search


def load(query, num_results=5):
    print(f"Searching for: '{query}'...")
    results = []
    try:
        for url in search(query, num_results=num_results):
            results.append(url)
    except Exception as e:
        print(f"Search failed: {e}")

    return results