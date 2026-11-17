"""
Отлично! Досье Пикачу найдено. Помимо базовых характеристик, у каждого покемона
есть так называемый «вид» (`species`), где хранится дополнительная интересная
информация — например, базовый уровень счастья (`base_happiness`).

Сделайте новый запрос к PokeAPI и распечатайте на экран данные об уровне
счастья Пикачу.
"""

import requests

response = requests.get(
    "https://pokeapi.co/api/v2/pokemon-species/25/", timeout=10
)
happiness = response.json()["base_happiness"]

print(happiness)
