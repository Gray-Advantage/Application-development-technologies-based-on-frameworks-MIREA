"""
В файле *models.py* приложения **core** создайте абстрактную модель
`PublishedModel`. Эта модель должна добавлять в модели-наследники флаг
`is_published` со значением по умолчанию `True`.

Импортируйте модель `PublishedModel` в файл *models.py* приложения
**ice_cream** и проведите рефакторинг кода: уберите из моделей `Category`,
`Topping`, `Wrapper` и `IceCream` повторяющиеся поля и примените наследование
от абстрактной модели.
"""

from django.db import models


class PublishedModel(models.Model):
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True
