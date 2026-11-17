"""Практика ветвлений — облицовка бассейна.

Функция count_tiles(dep, leng, wid=None) возвращает число плиток
размера метр на метр для четырёх стен и дна бассейна. Если ширина
не передана, считайте бассейн квадратным, ширина равна длине.
"""


def count_tiles(dep, leng, wid=None):
    if wid is None:
        wid = leng
    return 2 * dep * (leng + wid) + leng * wid


total_tiles_1 = count_tiles(2, 2)
print("Потребуется плиток:", total_tiles_1)
total_tiles_2 = count_tiles(1, 2, 3)
print("Потребуется плиток:", total_tiles_2)
total_tiles_3 = count_tiles(2, 5, 3)
print("Потребуется плиток:", total_tiles_3)
