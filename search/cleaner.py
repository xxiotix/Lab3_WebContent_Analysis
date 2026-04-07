def clean_url(url: str) -> str:
    """
    Видаляє http://, https:// та все після першого '/' після домену.
    """
    url = url.strip()
    # Прибираємо протокол
    for prefix in ("https://", "http://"):
        if url.startswith(prefix):
            url = url[len(prefix):]
            break
    # Відкидаємо все починаючи з першого '/'
    if "/" in url:
        url = url[:url.index("/")]
    return url.lower()


def deduplicate(domains: list[str]) -> list[str]:
    """
    Залишає перші входження, відкидає дублікати (зберігає порядок).
    """
    seen = set()
    result = []
    for d in domains:
        if d not in seen:
            seen.add(d)
            result.append(d)
    return result


def clean_results(raw_links: list[str]) -> list[str]:
    """
    Повний пайплайн: очистити URL → прибрати дублікати.
    """
    cleaned = [clean_url(link) for link in raw_links if link]
    return deduplicate(cleaned)