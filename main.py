"""Сервис сокращения ссылок.

Начальный программный сценарий проекта (ПР1): создание одной короткой
ссылки и вывод сведений о ней. В сценарии используются простые типы
данных, операции, преобразование типов, ветвления и импорт модулей.
"""

import hashlib
from datetime import date, timedelta

SERVICE_DOMAIN = "sl.mirea"
CODE_LENGTH = 6

original_url = "https://www.mirea.ru/education/programmy-obucheniya/"
custom_alias = "mirea"
is_alias_free = True
created_at = date(2026, 9, 1)
lifetime_days = 30
clicks_input = "128"


def get_link_status(is_available):
    """Вернуть текстовый статус короткого кода."""
    if is_available:
        return "Короткий код свободен, ссылку можно создать"
    return "Короткий код уже занят"


# Функция 1. Создание короткой ссылки.
# Короткий код формируется из хеша исходного адреса, но если
# пользователь задал собственный алиас и алиас свободен, то
# используется алиас.
url_hash = hashlib.md5(original_url.encode("utf-8")).hexdigest()
generated_code = url_hash[:CODE_LENGTH]

if is_alias_free and custom_alias != "":
    short_code = custom_alias
else:
    short_code = generated_code

short_url = "https://" + SERVICE_DOMAIN + "/" + short_code

# Функция 2. Проверка занятости короткого кода.
alias_status = get_link_status(is_alias_free)

# Функция 3. Проверка срока действия ссылки.
expires_at = created_at + timedelta(days=lifetime_days)
days_left = (expires_at - date.today()).days

if days_left > 7:
    lifetime_status = "Ссылка активна"
elif days_left > 0:
    lifetime_status = "Срок действия ссылки скоро истекает"
else:
    lifetime_status = "Срок действия ссылки истёк"

# Функция 4. Учёт переходов и статистика.
clicks = int(clicks_input)
days_passed = (date.today() - created_at).days

if days_passed > 0:
    clicks_per_day = clicks / days_passed
else:
    clicks_per_day = float(clicks)

is_popular = clicks >= 100 and days_left > 0

# Функция 5. Просмотр сведений о ссылке.
print("=== Сервис сокращения ссылок ===")
print("Исходный адрес: " + original_url)
print("Короткий адрес: " + short_url)
print("Короткий код: " + short_code)
print("Дата создания: " + str(created_at))
print("Действует до: " + str(expires_at))
print("Осталось дней: " + str(days_left))
print("Переходов: " + str(clicks))
print(f"Переходов в день: {clicks_per_day:.2f}")
print(alias_status)
print(lifetime_status)

if is_popular:
    print("Ссылка популярна: более 100 переходов")
else:
    print("Ссылка пока не набрала 100 переходов")
