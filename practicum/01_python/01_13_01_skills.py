"""Практика по теме — анализ дополнительных навыков разработчиков.

Напишите analyze_skills, которая находит минимум и максимум среди
заданных долей навыков. Напечатайте две строки с подписями
«Доля питонистов, у которых есть наименее популярный навык (в %):»
и «Доля питонистов, у которых есть наиболее популярный навык (в %):».
Название навыка не выводите, функция не должна возвращать значение.
"""

bash = 31
c_and_c_plus_plus = 29
c_sharp = 11
html_css = 36
java = 19
javascript = 37
sql = 34


def analyze_skills():
    minimum = min(
        bash, c_and_c_plus_plus, c_sharp, html_css, java, javascript, sql
    )
    maximum = max(
        bash, c_and_c_plus_plus, c_sharp, html_css, java, javascript, sql
    )
    print(
        "Доля питонистов, у которых есть наименее популярный навык (в %):",
        minimum,
    )
    print(
        "Доля питонистов, у которых есть наиболее популярный навык (в %):",
        maximum,
    )


analyze_skills()
