"""Практика циклов — участники автомобильного чемпионата.

analyze_results получает список словарей результатов гонок с одним
составом команд. Отсортируйте названия команд по алфавиту и напечатайте
заголовок «Команды, участвовавшие в чемпионате:», затем каждую команду
в отдельной строке с префиксом «* ».
"""


def analyze_results(data):
    teams = sorted(data[0])
    print("Команды, участвовавшие в чемпионате:")
    for team in teams:
        print("*", team)


races_data = [
    {"Ferrari": 20, "Mercedes": 5, "Aston Martin": 10, "Williams": 15},
    {"Mercedes": 15, "Aston Martin": 20, "Ferrari": 10, "Williams": 0},
    {"Ferrari": 20, "Williams": 15, "Aston Martin": 10, "Mercedes": 5},
]
analyze_results(races_data)
