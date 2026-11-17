"""
В файле *models.py* приложения **ice_cream** описаны четыре модели:

- `Category` — категории сортов мороженого; каждое мороженое принадлежит лишь
  одной категории; одной категории может принадлежать несколько сортов;
- `Topping` — добавки к мороженому; к каждому мороженому может прилагаться
  несколько топпингов;
- `Wrapper` — обёртки для мороженого; у каждого сорта мороженого может быть
  только одна обёртка;
- `IceCream` — сорта мороженого.

В модель `IceCream` добавьте поля, связывающие её с остальными моделями:

- **С моделью** `Category`:

  - имя поля: `category`;
  - тип связи: N:1;
  - обязательное поле;
  - при удалении категории должны быть удалены все сорта мороженого из этой
    категории

- **С моделью** `Topping`:

  - имя поля: `toppings`;
  - тип связи: N:M;
  - обязательное поле;

- **С моделью** `Wrapper`:

  - имя поля: `wrapper`;
  - тип связи: 1:1;
  - необязательное поле;
  - при удалении связанной записи в этом поле должно быть установлено `NULL`.
"""

from django.db import models


# Категории.
class Category(models.Model):
    is_published = models.BooleanField(default=True)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=64, unique=True)
    output_order = models.PositiveSmallIntegerField(default=100)


# Топпинги.
class Topping(models.Model):
    is_published = models.BooleanField(default=True)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=64, unique=True)


# Обёртки.
class Wrapper(models.Model):
    is_published = models.BooleanField(default=True)
    title = models.CharField(max_length=256)


# Сорта мороженого.
class IceCream(models.Model):
    is_published = models.BooleanField(default=True)
    is_on_main = models.BooleanField(default=False)
    title = models.CharField(max_length=256)
    description = models.TextField()
    wrapper = models.OneToOneField(
        Wrapper,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    toppings = models.ManyToManyField(Topping)
