SERP_API_KEY = "d5d72ba3a1d7f6a941f6dbf5e30060bd41fdc624a5e283ea5910a2d5b069d127"

# Кількість результатів від кожної пошукової системи
RESULTS_PER_ENGINE = 10

# Коефіцієнти для підходу №2 (формула 13) - задаються вручну якщо потрібно
# x1 та x2 обчислюються динамічно за формулою (16), тут лише запасні значення
X1_DEFAULT = 0.5
X2_DEFAULT = 0.5

# 5 пошукових рушіїв через SerpAPI
ENGINES = [
    "google",
    "bing",
    "duckduckgo",
    "brave_ai_mode",
    "baidu",
]

# Експертні оцінки кожного рушія E_i (від 0 до 1), індекс відповідає ENGINES
EXPERT_SCORES = {
    "google": 1.0,
    "bing": 0.8,
    "duckduckgo": 0.7,
    "brave_ai_mode": 0.7,
    "baidu": 0.6,
}