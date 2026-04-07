def print_separator(char="─", width=60):
    print(char * width)


def print_individual_results(rankings: dict[str, list[str]]):
    """Виводить результати від кожної пошукової системи окремо."""
    print_separator("═")
    print("  РЕЗУЛЬТАТИ ПОШУКУ ПО КОЖНІЙ СИСТЕМІ")
    print_separator("═")
    for engine, domains in rankings.items():
        print(f"\n  [{engine.upper()}]  ({len(domains)} результатів)")
        print_separator()
        if not domains:
            print("  (немає результатів)")
        else:
            for i, domain in enumerate(domains, 1):
                print(f"  {i:>3}. {domain}")
    print()


def print_weights(weights: dict[str, float], label: str):
    """Виводить ваги джерел інформації."""
    print_separator()
    print(f"  Ваги ІД ({label}):")
    print_separator()
    for engine, w in weights.items():
        bar = "█" * int(w * 30)
        print(f"  {engine:<12} {w:.4f}  {bar}")
    print()


def print_aggregated(result: list[str], method: str, weight_approach: str):
    """Виводить агреговане ранжирування."""
    print_separator("═")
    print(f"  АГРЕГОВАНЕ РАНЖИРУВАННЯ")
    print(f"  Метод: {method}  |  Ваги: {weight_approach}")
    print_separator("═")
    for i, domain in enumerate(result, 1):
        print(f"  {i:>3}. {domain}")
    print()