"""Создайте наследников Employee: FullTimeEmployee и PartTimeEmployee.

Оба класса хранят first_name, second_name, gender и remaining_vacation_days.
У FullTimeEmployee оплачиваемый отпуск равен 28 дням. Его дополнительный метод
get_unpaid_vacation(start_date, days) принимает строку даты и число дней,
возвращая сообщение:
Начало неоплачиваемого отпуска: <дата>, продолжительность: <число> дней.
В PartTimeEmployee переопределите атрибут класса vacation_days значением 14.
Сохраните унаследованные методы списания отпуска и получения его остатка.
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


class FullTimeEmployee(Employee):
    def get_unpaid_vacation(self, start_date, days):
        return (
            f"Начало неоплачиваемого отпуска: {start_date}, "
            f"продолжительность: {days} дней."
        )


class PartTimeEmployee(Employee):
    vacation_days = 14


full_time_employee = FullTimeEmployee("Роберт", "Крузо", "м")
print(full_time_employee.get_unpaid_vacation("2023-07-01", 5))
part_time_employee = PartTimeEmployee("Алёна", "Пятницкая", "ж")
print(part_time_employee.get_vacation_details())
