from config import EXPERT_SCORES, ENGINES

# Допоміжні величини
def compute_Vi(rankings: dict[str, list[str]]) -> dict[str, float]:
    """
    Vi = mi / sum(mk) - видана частка знайдених результатів надана ІД (формула 11).
    """
    total = sum(len(v) for v in rankings.values())
    if total == 0:
        return {e: 0.0 for e in rankings}
    return {engine: len(domains) / total for engine, domains in rankings.items()}


def compute_Oi(rankings: dict[str, list[str]]) -> dict[str, float]:
    """
    Oi = mi / P - де P — кількість унікальних альтернатив (формула 12).
    """
    all_alts = set()
    for domains in rankings.values():
        all_alts.update(domains)
    P = len(all_alts)
    if P == 0:
        return {e: 0.0 for e in rankings}
    return {engine: len(domains) / P for engine, domains in rankings.items()}


def compute_rho(rankings: dict[str, list[str]]) -> float:
    """
    ρ = (sum hj) / (n * P) - щільність перетину результатів (формула 15).
    hj - кількість ІД, що надали j-ту альтернативу.
    """
    n = len(rankings)
    all_alts: dict[str, int] = {}
    for domains in rankings.values():
        for d in domains:
            all_alts[d] = all_alts.get(d, 0) + 1

    P = len(all_alts)
    if P == 0 or n == 0:
        return 1.0 / n if n > 0 else 0.0

    sum_hj = sum(all_alts.values())
    return sum_hj / (n * P)


def _normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    """Нормалізує ваги до суми 1."""
    total = sum(weights.values())
    if total == 0:
        return {e: 1 / len(weights) for e in weights}
    return {e: w / total for e, w in weights.items()}

# Підхід №2 (формула 13)
def weights_approach2(rankings: dict[str, list[str]]) -> dict[str, float]:
    """
    wi = Ei * (x1*Oi + x2*Vi)
    x2 = ρ,  x1 = 1 - ρ   (формула 16)
    """
    Vi = compute_Vi(rankings)   # взаємооцінка
    Oi = compute_Oi(rankings)   # об'єктивна оцінка
    rho = compute_rho(rankings) # щільність перетину

    x2 = rho
    x1 = 1.0 - rho

    weights = {}
    for engine in rankings:
        Ei = EXPERT_SCORES.get(engine, 0.5)
        weights[engine] = Ei * (x1 * Oi[engine] + x2 * Vi[engine])

    return _normalize_weights(weights)

# Підхід №3 — статистичний (формула 17)
def weights_approach3(rankings: dict[str, list[str]]) -> dict[str, float]:
    """
    x1 = D(V),  x2 = 1 - x1
    wi = Ei * (x1*Oi + x2*Vi)
    """
    Vi = compute_Vi(rankings)
    Oi = compute_Oi(rankings)

    v_values = list(Vi.values())
    n = len(v_values)

    # Дисперсія D(V) = M(V^2) - (M(V))^2
    mean_v  = sum(v_values) / n
    mean_v2 = sum(v ** 2 for v in v_values) / n
    d_v = mean_v2 - mean_v ** 2

    # Обмежуємо в [0, 1]
    x1 = min(max(d_v, 0.0), 1.0)
    x2 = 1.0 - x1

    weights = {}
    for engine in rankings:
        Ei = EXPERT_SCORES.get(engine, 0.5)
        weights[engine] = Ei * (x1 * Oi[engine] + x2 * Vi[engine])

    return _normalize_weights(weights)