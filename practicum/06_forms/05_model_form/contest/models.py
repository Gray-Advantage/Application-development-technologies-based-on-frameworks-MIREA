"""
Перепишите форму для конкурса мороженого с использованием класса `ModelForm`.
Для этого в файле *contest/models.py* создайте модель `Contest`, где по
аналогии с существующей формой `ContestForm` опишите поля модели.

Для полей `description` и `comment` установите подходящий класс для текста.
Список встроенных полей для моделей можно посмотреть [в
документации](https://docs.djangoproject.com/en/5.2/ref/models/fields/#field-t\
ypes){target="blank"}.
В классе `Form` нет текстового типа поля, есть только текстовый виджет. Но вот
в моделях есть разные классы для строк и текста.

Для валидации целочисленного поля `price` используйте валидаторы, описанные [в
документации](https://docs.djangoproject.com/en/5.2/ref/models/fields/#integer\
field){target="blank"}.
Пример использования валидаторов найдите самостоятельно — в документации или на
тематических ресурсах в сети.

В классе формы опишите виджеты для многострочных полей ввода, иначе эти поля
получатся слишком высокими.

В результате вашей работы форма должна выглядеть так:

![](https://pictures.s3.yandex.net:443/resources/152_1_1682598331.png)

Чтобы форма заработала, создавать и применять миграции не обязательно: форма
будет работать и без этого. А в задании нам большего и не надо.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Contest(models.Model):
    title = models.CharField("Название", max_length=20)
    description = models.TextField("Описание")
    price = models.IntegerField(
        "Цена",
        validators=[MinValueValidator(10), MaxValueValidator(100)],
        help_text="Рекомендованная розничная цена",
    )
    comment = models.TextField("Комментарий", blank=True)
