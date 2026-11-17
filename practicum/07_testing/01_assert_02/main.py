"""
Протестируйте методы `programmer_define()` и `age_define()` класса `Contact`.

Тестировать нужно все возможные варианты: в метод `programmer_define()` по
очереди передайте `False` и `True`, а в `age_define()` проверьте три возрастные
категории.

Для проверки всех возможных вариантов создайте несколько экземпляров класса
`Contact` с разными значениями полей `year_birth` и `is_programmer`.
"""


class Contact:

    def __init__(self, name, year_birth, is_programmer):
        self.name = name
        self.year_birth = year_birth
        self.is_programmer = is_programmer

    def age_define(self):
        if 1946 < self.year_birth < 1980:
            return "Олдскул"
        if self.year_birth >= 1980:
            return "Молодой"
        return "Старейшина"

    def programmer_define(self):
        if self.is_programmer:
            return "Программист"
        return "Нормальный"

    def show_contact(self):
        return (
            f"{self.name}, "
            f"возраст: {self.age_define()}, "
            f"статус: {self.programmer_define()}"
        )


# Проверяем оба статуса и все три возрастные категории.
test_none_programmer: Contact = Contact("имя", 0, False)
assert (
    test_none_programmer.programmer_define() == "Нормальный"
), "В programmer_define() статус «Нормальный» не работает"
assert (
    test_none_programmer.age_define() == "Старейшина"
), "В age_define() категория «Старейшина» не работает"

test_oldschool: Contact = Contact("Олдскул", 1947, True)
assert (
    test_oldschool.programmer_define() == "Программист"
), "В programmer_define() статус «Программист» не работает"
assert (
    test_oldschool.age_define() == "Олдскул"
), "В age_define() категория «Олдскул» не работает"

test_young: Contact = Contact("Молодой", 1980, False)
assert (
    test_young.programmer_define() == "Нормальный"
), "В programmer_define() статус «Нормальный» не работает"
assert (
    test_young.age_define() == "Молодой"
), "В age_define() категория «Молодой» не работает"

# Проверяем оставшиеся годы на границах возрастных категорий.
test_elder_boundary: Contact = Contact("Старейшина", 1946, True)
assert (
    test_elder_boundary.age_define() == "Старейшина"
), "В age_define() неверно определяется категория для 1946 года"

test_oldschool_boundary: Contact = Contact("Олдскул", 1979, False)
assert (
    test_oldschool_boundary.age_define() == "Олдскул"
), "В age_define() неверно определяется категория для 1979 года"
