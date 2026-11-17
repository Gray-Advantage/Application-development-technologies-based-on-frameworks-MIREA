"""Добавьте в Employee атрибут класса vacation_days со значением 28.

При создании объекта задавайте атрибуты first_name, second_name и gender.
Создайте employee1 и employee2 с различными именем, фамилией и полом.
Напечатайте данные каждого сотрудника через f-строку в формате:
Имя: Роберт, Фамилия: Крузо, Пол: м, Отпускных дней в году: 28.
"""


class Employee:
    vacation_days = 28

    def __init__(self, first_name, second_name, gender):
        self.first_name = first_name
        self.second_name = second_name
        self.gender = gender


employee1 = Employee("Роберт", "Крузо", "м")
employee2 = Employee("Алёна", "Пятницкая", "ж")

print(
    f"Имя: {employee1.first_name}, Фамилия: {employee1.second_name}, "
    f"Пол: {employee1.gender}, "
    f"Отпускных дней в году: {employee1.vacation_days}."
)
print(
    f"Имя: {employee2.first_name}, Фамилия: {employee2.second_name}, "
    f"Пол: {employee2.gender}, "
    f"Отпускных дней в году: {employee2.vacation_days}."
)
