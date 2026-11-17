"""Числа Фибоначчи — это последовательность чисел, где первые два числа — это 0
и 1, а каждое последующее число вычисляется как сумма двух предыдущих.

Например, вот первые шесть чисел последовательности Фибоначчи:

```
0, 1, 1, 2, 3, 5
```

Напишите функцию-генератор `fibonacci(n)`, которая вычисляет элементы
последовательности Фибоначчи до n-ого числа.
"""


def fibonacci(n):
    current, following = 0, 1
    for _ in range(n):
        yield current
        current, following = following, current + following


sequence = fibonacci(10)
for number in sequence:
    print(number)
