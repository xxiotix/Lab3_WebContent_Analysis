from config import ENGINES
from search.serp_client import fetch_results
from search.cleaner import clean_results


def search_all(query: str) -> dict[str, list[str]]:
    """
    Надсилає запит до всіх 5 рушіїв.
    Повертає словник  { engine_name: [domain1, domain2, ...] }
    """
    results = {}
    for engine in ENGINES:
        print(f"  → Запит до: {engine}...")
        raw_links = fetch_results(query, engine)
        domains = clean_results(raw_links)
        results[engine] = domains
    return results