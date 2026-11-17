"""Практика циклов — победитель автомобильного чемпионата.

Расширьте analyze_results: после алфавитного списка команд напечатайте
«В чемпионате победила команда <название> с результатом <сумма> баллов».
Суммируйте очки всех заездов в словаре scores, затем найдите победителя.
"""


def analyze_results(data):
    teams = sorted(data[0])
    print("Команды, участвовавшие в чемпионате:")
    for team in teams:
        print("*", team)
    scores = {}
    for race in data:
        for team, score in race.items():
            if team in scores:
                scores[team] += score
            else:
                scores[team] = score
    winner_team = None
    winner_score = 0
    for team, score in scores.items():
        if winner_team is None or score > winner_score:
            winner_team = team
            winner_score = score
    print(
        "В чемпионате победила команда",
        winner_team,
        "с результатом",
        winner_score,
        "баллов",
    )


races_data = [
    {"Ferrari": 20, "Mercedes": 5, "Aston Martin": 10, "Williams": 15},
    {"Mercedes": 15, "Aston Martin": 20, "Ferrari": 10, "Williams": 0},
    {"Ferrari": 20, "Williams": 15, "Aston Martin": 10, "Mercedes": 5},
]
analyze_results(races_data)
