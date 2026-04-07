def borda_aggregate(rankings: dict[str, list[str]], weights:  dict[str, float],) -> list[str]:
    """
    Проблема:
    Різні ІД можуть видавати різні набори альтернатив.

    Алгоритм уніфікації:
    Крок 1. Шукаємо всі унікальні альтернативи. Виходить множина розміром M.
    Крок 2. Кожному ІД дописати відсутні альтернативи з рангом m_i+1.
    Крок 3. Підсумувати ранги.
    Крок 4. Відсортувати за зростанням суми.

    """

    # Крок 1
    all_alts: list[str] = [] # список унікальних альтернатив
    seen = set()                # множина унікальних альтернатив
    for domains in rankings.values():
        for d in domains:
            if d not in seen:
                seen.add(d)            # Додаємо до множини (не зберігає порядок)
                all_alts.append(d)  # Додаємо до списку (зберігає порядок)

    # Крок 2
    scores: dict[str, float] = {alt: 0.0 for alt in all_alts}

    for engine, domains in rankings.items():
        w = weights.get(engine, 0.0)      # Ваги ІД; якщо нема, то 0.0
        mi = len(domains)                        # Довжина ранжування
        penalty = mi + 1                         # Штрафний ранг

        rank_map = {d: (i + 1) for i, d in enumerate(domains)}  # альтернатива: ранг

        for alt in all_alts:
            r = rank_map.get(alt, penalty)       #Якщо альтернатива є, беремо ранг; якщо ні - штрафний ранг
            scores[alt] += w * r                 # Крок 3

    # Крок 4
    ranked = sorted(all_alts, key=lambda a: scores[a])
    return ranked