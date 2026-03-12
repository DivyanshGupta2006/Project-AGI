from ddgs import DDGS

def load(query, max_results=20):
    print(f"Searching...")
    results = []
    try:
        with DDGS() as ddgs:
            ddg_gen = ddgs.text(query, max_results=max_results)

            for r in ddg_gen:
                formatted_result = f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n"
                results.append(formatted_result)

    except Exception as e:
        print(f"DDG Search failed: {e}")

    return "\n".join(results) if results else "No results found."