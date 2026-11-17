"""Дополните Employee методами учёта оставшихся отпускных дней.

Атрибут класса vacation_days равен 28. В __init__ сохраняйте first_name,
second_name, gender и remaining_vacation_days, изначально равный vacation_days.
Метод consume_vacation(days) уменьшает remaining_vacation_days на days.
Метод get_vacation_details() возвращает строку:
Остаток отпускных дней: <число>.
Создайте сотрудника, спишите 7 дней и выведите остаток.
"""


class Employee:
    vacation_days = 28

    def __init__(self, first_name, second_name, gender):
        self.first_name = first_name
        self.second_name = second_name
        self.gender = gender
        self.remaining_vacation_days = self.vacation_days

    def consume_vacation(self, days):
        self.remaining_vacation_days -= days

    def get_vacation_details(self):
        return f"Остаток отпускных дней: {self.remaining_vacation_days}."


employee = Employee("Роберт", "Крузо", "м")
employee.consume_vacation(7)
print(employee.get_vacation_details())
