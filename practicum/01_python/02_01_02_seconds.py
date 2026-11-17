"""Числовые типы — перевод секунд.

Переведите 424562 секунды в сутки, часы, минуты и секунды.
Не изменяйте total_seconds. Выведите исходное значение и результат
в отдельных строках с подписями «Суток:», «Часов:», «Минут:», «Секунд:».
"""

total_seconds = 424562
days = total_seconds // (24 * 60 * 60)
hours = total_seconds // (60 * 60) % 24
minutes = total_seconds // 60 % 60
seconds = total_seconds % 60

print(total_seconds, "секунд - это")
print("Суток:", days)
print("Часов:", hours)
print("Минут:", minutes)
print("Секунд:", seconds)
