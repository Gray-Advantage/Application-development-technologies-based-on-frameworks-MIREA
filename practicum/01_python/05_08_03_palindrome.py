"""Практика коллекций — палиндром.

is_palindrome принимает строку из букв, цифр и пробелов и возвращает,
читается ли она одинаково слева направо и справа налево.
Игнорируйте регистр и пробелы. Для проверки примените срез строки.
"""


def is_palindrome(text):
    normalized = text.lower().replace(" ", "")
    return normalized == normalized[::-1]


print(is_palindrome("А роза упала на лапу Азора"))
print(is_palindrome("Не палиндром"))
