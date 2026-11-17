"""
В файле *models.py* приложения **ice_cream** создайте модель **Category**
(категории сортов мороженого).

Поля модели:

- `title` — строка (не более 256 символов)
- `slug` — поле типа *slug* (не более 64 символов, уникальное в пределах
  таблицы)
- `output_order` — целочисленное поле с ограничением значений от 0 до 32767
  (значение по умолчанию — 100)
- `is_published` — булев тип (по умолчанию — `True`)

Поле `output_order` — это «вес» записи, определяющий порядок её отображения на
странице проекта; в дальнейшем с помощью этого поля, используя `ORDER BY`,
администратор сможет менять порядок вывода данных на веб-страницу: чем меньше
«вес» записи — тем выше она отобразится («лёгкое — всплывает»).
"""

from django.db import models


# Категории
class Category(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=64, unique=True)
    output_order = models.PositiveSmallIntegerField(default=100)
    is_published = models.BooleanField(default=True)


# Топпинги
class Topping(models.Model):
    is_published = models.BooleanField(default=True)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=64, unique=True)


# Обёртки
class Wrapper(models.Model):
    is_published = models.BooleanField(default=True)
    title = models.CharField(max_length=256)


# Сорта мороженого
class IceCream(models.Model):
    is_published = models.BooleanField(default=True)
    is_on_main = models.BooleanField(default=False)
    title = models.CharField(max_length=256)
    description = models.TextField()
