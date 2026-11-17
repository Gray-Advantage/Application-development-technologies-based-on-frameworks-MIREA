"""
Среди всего многообразия покемонов нам нужен самый знаменитый. Найдите Пикачу
(pikachu) через API и напечатайте в терминале информацию о его базовом весе
(ключ `weight`).

PokeAPI предоставляет отличную возможность искать покемонов, добавляя их имя
прямо в URL запроса.
"""

from pprint import pprint

import requests

response = requests.get(
    "https://pokeapi.co/api/v2/pokemon/pikachu/", timeout=10
)
weight = response.json()["weight"]
pprint(weight)
