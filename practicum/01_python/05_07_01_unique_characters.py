"""Подсчитайте уникальные символы строки, не учитывая пробелы.

Дана original_phrase = «съешь же ещё этих мягких французских булок
да выпей чаю». Создайте множество uniq_chars из символов строки,
удалите элемент ' ', вычислите число оставшихся элементов
в uniq_chars_count и напечатайте его.
"""

original_phrase = "съешь же ещё этих мягких французских булок да выпей чаю"
uniq_chars = set(original_phrase)
set.discard(uniq_chars, " ")
uniq_chars_count = len(uniq_chars)
print(uniq_chars_count)
