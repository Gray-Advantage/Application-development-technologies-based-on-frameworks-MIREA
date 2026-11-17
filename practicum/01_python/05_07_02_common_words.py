"""Найдите количество уникальных слов, общих для двух строк.

Напишите find_common_words_count(first_string, second_string).
Слова разделены пробелами: разбейте строки на списки слов,
преобразуйте списки во множества, найдите пересечение и верните
его длину. Повторы слова в строке не увеличивают результат.
Например, для «наш кот ест суп» и «тёк под пол наш суп это всё наш кот»
нужно вернуть 3. Вызовите функцию с phrase_1 и phrase_2, сохраните
результат в common_words_count и напечатайте его после сообщения
«Общих уникальных слов в предложениях:».
"""


def find_common_words_count(first_string, second_string):
    first_words = first_string.split()
    second_words = second_string.split()
    first_words_set = set(first_words)
    second_words_set = set(second_words)
    common_words = first_words_set & second_words_set
    return len(common_words)


phrase_1 = "кот зол как лев дай мне сыр дай мне суп"
phrase_2 = "кто ест сыр тот кот кто ест суп тот нет"

common_words_count = find_common_words_count(phrase_1, phrase_2)
print("Общих уникальных слов в предложениях:", common_words_count)
