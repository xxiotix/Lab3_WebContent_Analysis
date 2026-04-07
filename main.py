import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from search.engines import search_all
from aggregation.weights import weights_approach2, weights_approach3
from aggregation.borda import borda_aggregate
from aggregation.condorcet import condorcet_aggregate
from utils.display import (
    print_individual_results,
    print_weights,
    print_aggregated,
)


def main():
    print("=" * 60)
    print("  МЕТАПОШУКОВА СИСТЕМА — Лабораторна робота №3")
    print("=" * 60)

    query = input("\n  Введіть пошуковий запит: ").strip()
    if not query:
        print("  Запит порожній. Завершення.")
        return

    print(f"\n  Пошук за запитом: «{query}»\n")

    # 1. Отримати результати від 5 пошукових систем
    rankings = search_all(query)

    # 2. Вивести індивідуальні результати
    print_individual_results(rankings)

    # 3. Обчислити ваги двома підходами
    w2 = weights_approach2(rankings)
    w3 = weights_approach3(rankings)

    print_weights(w2, "Підхід №2 (кількість та якість)")
    print_weights(w3, "Підхід №3 (статистичний)")

    # 4. Борда + Підхід №2
    result_b2 = borda_aggregate(rankings, w2)
    print_aggregated(result_b2, "Борда (модифікований)", "Підхід №2")

    # 5. Борда + Підхід №3
    result_b3 = borda_aggregate(rankings, w3)
    print_aggregated(result_b3, "Борда (модифікований)", "Підхід №3")

    # 6. Кондорсе + Підхід №2
    result_c2 = condorcet_aggregate(rankings, w2)
    print_aggregated(result_c2, "Кондорсе (модифікований)", "Підхід №2")

    # 7. Кондорсе + Підхід №3
    result_c3 = condorcet_aggregate(rankings, w3)
    print_aggregated(result_c3, "Кондорсе (модифікований)", "Підхід №3")


if __name__ == "__main__":
    main()