def condorcet_aggregate(
    rankings: dict[str, list[str]],
    weights:  dict[str, float],
) -> list[str]:
    """
    Алгоритм:
    1. Шукаємо всі унікальні альтернативи. Виходить множина розміром M.
    2. Для кожного ІД побудувати матрицю ординальних порівнянь d^(j)_ik:
         +1 якщо Ai > Ak (Ai стоїть вище, тобто менший ранг)
         -1 якщо Ai < Ak
          0 якщо однакові ранги (або обидва відсутні)
    3. Обчислити зважену суму: S_ik = sum_j(wj * d^(j)_ik)
    4. Побудувати підсумкову матрицю D:
         d_ik = +1 якщо S_ik > 0
         d_ik = -1 якщо S_ik < 0
         d_ik = 0 якщо S_ik = 0
    5. Підрахувати рядкові суми sum_k(d_ik) для кожної альтернативи.
    6. Відсортувати за спаданням суми (більша сума → вищий ранг).
    """

    # Крок 1: уніфікована множина
    all_alts: list[str] = []
    seen = set()
    for domains in rankings.values():
        for d in domains:
            if d not in seen:
                seen.add(d)
                all_alts.append(d)

    M = len(all_alts)
    if M == 0:
        return []

    idx = {alt: i for i, alt in enumerate(all_alts)}

    # Крок 2-3: зважена матриця S (MxM)
    S = [[0.0] * M for _ in range(M)]

    for engine, domains in rankings.items():
        w = weights.get(engine, 0.0)
        mi = len(domains)
        penalty = mi + 1

        rank_map = {d: (i + 1) for i, d in enumerate(domains)}

        for a in range(M):
            for k in range(M):
                if a == k:
                    continue
                ai = all_alts[a]
                ak = all_alts[k]
                r_ai = rank_map.get(ai, penalty)
                r_ak = rank_map.get(ak, penalty)

                if r_ai < r_ak:       # ai перевищує ak
                    S[a][k] += w
                elif r_ai > r_ak:     # ai поступається ak
                    S[a][k] -= w
                # якщо рівні — 0, нічого не додаємо

    # Крок 4: підсумкова матриця D
    D = [[0] * M for _ in range(M)]
    for a in range(M):
        for k in range(M):
            if S[a][k] > 0:
                D[a][k] = 1
            elif S[a][k] < 0:
                D[a][k] = -1

    # Крок 5: рядкові суми
    row_scores = [sum(D[a]) for a in range(M)]

    # Крок 6: сортування за спаданням
    ranked = sorted(all_alts, key=lambda alt: row_scores[idx[alt]], reverse=True)
    return ranked