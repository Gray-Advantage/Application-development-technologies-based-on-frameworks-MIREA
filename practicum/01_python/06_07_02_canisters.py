"""Практика циклов — запас питьевой воды.

count_canisters получает список среднесуточных температур и возвращает
количество дней с температурой не ниже 30 градусов. Вызовите функцию
для forecast_temperatures и напечатайте «Нужно канистр: <число>».
"""


def count_canisters(temperatures_per_day):
    hot_days_counter = 0
    for temperature in temperatures_per_day:
        if temperature >= 30:
            hot_days_counter += 1
    return hot_days_counter


forecast_temperatures = [26, 28, 30, 31, 29, 31, 28, 26]
print("Нужно канистр:", count_canisters(forecast_temperatures))
