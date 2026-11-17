"""Практика по теме — исправление программы Hello World.

Исправьте отступы, возвращаемое значение say_world, объявите world_text
и выведите собранную строку «Hello, World!» через print.
say_hello возвращает «Hello», say_world возвращает «World!».
"""


def say_hello():
    return "Hello"


def say_world():
    return "World!"


hello_text = say_hello()
world_text = say_world()
result = hello_text + ", " + world_text
print(result)
