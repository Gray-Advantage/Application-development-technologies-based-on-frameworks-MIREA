"""Практика ветвлений — вместимость бассейна.

check_pool_capacity(num, leng, wid=None) возвращает, поместятся ли люди
при норме не более двух человек на квадратный метр. Неуказанная ширина
равна длине. Отрицательные аргументы преобразуйте в положительные.
Если площадь равна нулю, сразу верните False.
"""


def check_pool_capacity(num, leng, wid=None):
    num = abs(num)
    leng = abs(leng)
    if wid is None:
        wid = leng
    else:
        wid = abs(wid)
    area = leng * wid
    if area == 0:
        return False
    return num <= area * 2


def show_result(is_ok):
    if is_ok:
        print("Все люди из очереди поместятся в бассейн.")
    else:
        print("Люди из очереди не поместятся в бассейн.")


is_capacity_ok = check_pool_capacity(4, 2)
show_result(is_capacity_ok)
is_capacity_ok = check_pool_capacity(25, 5, 2)
show_result(is_capacity_ok)
