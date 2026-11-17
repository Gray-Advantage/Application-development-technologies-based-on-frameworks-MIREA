"""Практика коллекций — сравнение коллекций стикеров.

get_stickers_comparison принимает два списка и возвращает кортеж
из трёх отсортированных по алфавиту списков без повторов: стикеры
только первого владельца, только второго и общие для обоих.
"""


def get_stickers_comparison(collection_1, collection_2):
    first = set(collection_1)
    second = set(collection_2)
    return (
        sorted(first - second),
        sorted(second - first),
        sorted(first & second),
    )


stas_collection = [
    "Тим Бернерс-Ли",
    "Линус Торвальдс",
    "Ада Лавлейс",
    "Линус Торвальдс",
    "Маргарет Гамильтон",
    "Бьярн Страуструп",
]
anton_collection = [
    "Тим Бернерс-Ли",
    "Гвидо ван Россум",
    "Линус Торвальдс",
    "Бьярн Страуструп",
    "Бьярн Страуструп",
    "Кен Томпсон",
    "Деннис Ричи",
]

# Вызываем функцию и распаковываем полученный кортеж в три переменные:
stas_stickers, anton_stickers, common_stickers = get_stickers_comparison(
    stas_collection, anton_collection
)
# Печатаем результаты:
print("Стикеры, которые есть только у Стаса:", stas_stickers)
print("Стикеры, которые есть только у Антона:", anton_stickers)
print("Стикеры, которые есть и у Стаса, и у Антона:", common_stickers)
