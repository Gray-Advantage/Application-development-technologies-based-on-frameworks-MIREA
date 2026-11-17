"""Доработайте Employee и его наследника OfficeEmployee.

Employee хранит first_name, last_name, gender и remaining_vacation_days;
неизменный атрибут класса vacation_days равен 28. Добавьте защищённый атрибут
_employee_id и приватный метод __generate_employee_id(), возвращающий hash()
конкатенации имени, фамилии и пола. Сохраните списание и получение остатка.
OfficeEmployee дополнительно принимает worker_class и salary, хранит разряд
в worker_class, а зарплату в приватном атрибуте __salary.
Начальный остаток отпуска: vacation_days + 2 * worker_class.
Метод get_vacation_payment(days) возвращает целое число: за каждый день
отпуска выплачивается 1/60 зарплаты. Сохраните данные и сообщения примера.
"""


class Employee:
    vacation_days: int = 28

    def __init__(
        self,
        first_name: str,
        last_name: str,
        gender: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.remaining_vacation_days = self.vacation_days
        self._employee_id = self.__generate_employee_id()

    def __generate_employee_id(self) -> int:
        return hash(self.first_name + self.last_name + self.gender)

    def consume_vacation(self, days: int):
        self.remaining_vacation_days -= days

    def get_remaining_vacation_days(self) -> int:
        return self.remaining_vacation_days


class OfficeEmployee(Employee):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        gender: str,
        worker_class: int,
        salary: int,
    ):
        super().__init__(first_name, last_name, gender)
        self.worker_class = worker_class
        self.remaining_vacation_days = (
            self.vacation_days + 2 * self.worker_class
        )
        self.__salary = salary

    def get_vacation_payment(self, days: int) -> int:
        return int(self.__salary / 60 * days)


# Пример использования:
office_employee = OfficeEmployee(
    first_name="Иван",
    last_name="Иванов",
    gender="м",
    worker_class=2,
    salary=45000,
)

vacation_days = 10

office_employee.consume_vacation(vacation_days)

remaining_days = office_employee.get_remaining_vacation_days()
print(f"У сотрудника осталось {remaining_days} дн. отпуска.")

vacation_payment = office_employee.get_vacation_payment(vacation_days)
print(
    f"За {vacation_days} дн. отпуска сотрудник получит {vacation_payment} руб."
)
