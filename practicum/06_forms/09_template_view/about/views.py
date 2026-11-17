"""
Настройте страницу *about/* «О проекте»: замените view-функцию на CBV и
выведите на страницу общее число заявок, отправленных на конкурс рецептов.

В тренажёре эта страница формируется view-функцией, переделайте её на CBV. Для
этого в файле */about/views.py* создайте класс `Description`. Исправьте маршрут
в файле */about/urls.py*.

В качестве шаблона используйте тот же шаблон, что и был:
*about/description.html*. Сейчас страница «О проекте» выглядит так:

![скриншот веб-страницы. Заголовок "О проекте". Текст: "Каталог экзотических
сортов мороженного. Мы проводим конкурс рецептов мороженного среди наших
друзей. Количество поданных заявок:" Внизу страницы футер с названием
компании](https://pictures.s3.yandex.net:443/resources/249_1682626223.png)

Доработайте шаблон и напишите CBV так, чтобы в последней строке после двоеточия
выводилось количество поданных заявок — просто цифра без какого-либо
форматирования.
"""

from django.views.generic import TemplateView

from contest.models import Contest


class Description(TemplateView):
    template_name = "about/description.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contest_count"] = Contest.objects.count()
        return context
