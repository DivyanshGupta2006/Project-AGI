from ddgs import DDGS

def load(query, max_results=5):
    print(f"Searching...")
    results = []
    try:
        with DDGS() as ddgs:
            ddg_gen = ddgs.text(query, max_results=max_results)

            for r in ddg_gen:
                results.append(r['href'])

    except Exception as e:
        print(f"DDG Search failed: {e}")

    return results