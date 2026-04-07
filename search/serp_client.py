import requests
from config import SERP_API_KEY, RESULTS_PER_ENGINE

SERP_API_URL = "https://serpapi.com/search"


def fetch_results(query: str, engine: str) -> list[str]:
    """
    Запит до SerpAPI для заданого рушія.
    Повертає список сирих URL (до очищення).
    """
    params = {
        "q":        query,
        "engine":   engine,
        "api_key":  SERP_API_KEY,
        "num":      RESULTS_PER_ENGINE,
    }

    # Baidu використовує інший параметр для кількості результатів
    if engine == "baidu":
        params["rn"] = RESULTS_PER_ENGINE

    try:
        response = requests.get(SERP_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"  [!] Помилка запиту до '{engine}': {e}")
        return []
    except ValueError:
        print(f"  [!] Не вдалось розпарсити відповідь від '{engine}'")
        return []

    return _extract_links(data, engine)


def _extract_links(data: dict, engine: str) -> list[str]:
    """
    Витягує посилання з відповіді SerpAPI.
    Структура однакова для більшості рушіїв — поле 'organic_results'.
    """
    links = []

    organic = data.get("organic_results", [])
    for item in organic:
        link = item.get("link") or item.get("url", "")
        if link:
            links.append(link)

    return links