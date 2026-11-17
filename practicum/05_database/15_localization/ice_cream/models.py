"""
Повторите практические задания урока в тренажёре: локализуйте и переведите
админ-зону; настройте отображение элементов.

Вот что нужно сделать:

1. Перевести интерфейс админки на русский язык.
2. Перевести название приложения ICE_CREAM: в админ-зоне должно отображаться
название *Каталог мороженого*.
3. Перевести названия моделей:
- Category — «Категории»
- Topping — «Топпинги»
- Wrapper — «Обёртки»
- IceCream — «Мороженое»
4. Перевести названия полей в админке:
- Category
is_published — «Опубликовано»
title — «Название»
slug — «Слаг»
output_order — «Порядок отображения»
- Topping
is_published — «Опубликовано»
title — «Название»
slug — «Слаг»
- IceCream
is_published — «Опубликовано»
is_on_main — «На главную»
title — «Название»
description — «Описание»
- Wrapper
is_published — «Опубликовано»
title — «Название»
5. Настроить отображение объектов так, чтобы в списке объектов вместо *IceCream
object (1)* отображалось название мороженого (значение поля `title`). Таким же
образом надо настроить и остальные модели приложения **ice_cream**.
"""

from django.db import models

from core.models import PublishedModel


class Category(PublishedModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

    title = models.CharField("Название", max_length=256)
    slug = models.SlugField("Слаг", max_length=64, unique=True)
    output_order = models.PositiveSmallIntegerField(
        "Порядок отображения", default=100
    )


class Topping(PublishedModel):
    class Meta:
        verbose_name = "Топпинг"
        verbose_name_plural = "Топпинги"

    def __str__(self):
        return self.title

    title = models.CharField("Название", max_length=256)
    slug = models.SlugField("Слаг", max_length=64, unique=True)


class Wrapper(PublishedModel):
    class Meta:
        verbose_name = "Обёртка"
        verbose_name_plural = "Обёртки"

    def __str__(self):
        return self.title

    title = models.CharField("Название", max_length=256)


class IceCream(PublishedModel):
    class Meta:
        verbose_name = "Мороженое"
        verbose_name_plural = "Мороженое"

    def __str__(self):
        return self.title

    is_on_main = models.BooleanField("На главную", default=False)
    title = models.CharField("Название", max_length=256)
    description = models.TextField("Описание")
    wrapper = models.OneToOneField(
        Wrapper,
        on_delete=models.SET_NULL,
        related_name="ice_cream",
        null=True,
        blank=True,
        verbose_name="Обёртка",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="ice_creams",
        verbose_name="Категория",
    )
    toppings = models.ManyToManyField(Topping, verbose_name="Топпинги")
