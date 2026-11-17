"""
Настройте сохранение заявок на конкурс мороженого в базу данных.

После сохранения заявки её ID должен отображаться под формой, как на скриншоте:

![скриншот веб-страницы "Конкурс" с формой. Поля Название, Описание, Цена,
Комментарий. Кнопка Отправить. Надпись после отправки: "Рецепт мороженного
Мороженое-газировка принят на конкурс. Номер заявки: 6". Внизу ссылка "Список
всех заявок"](https://pictures.s3.yandex.net:443/resources/161_1682598719.png)

Выведите все сохранённые заявки на страницу *contest/list/*. Маршрут для этой
страницы уже подготовлен, а в директории *templates/contest/* лежит заготовка
HTML-шаблона.

При выводе на страницу заявки должны быть отсортированы по `id`.

Информация о каждой заявке должна быть обёрнута в HTML-тег `<div>`. Выведите
все поля каждой заявки, содержимое полей должно быть разделено запятыми.

Для примера:

| **id** | **title** | **price** | **description** | **comment** |
| --- | --- | --- | --- | --- |
| 12 | Арктический костёр | 68 | Пломбир с перцем чили | Зажигает даже в
сугробе |

Эта заявка в HTML-коде должна выглядеть так:

```html
...
<div>
12, Арктический костёр, 68, Пломбир с перцем чили, Зажигает даже в сугробе
</div>
...
```
"""

from django.shortcuts import render

from .forms import ContestForm
from .models import Contest


def proposal(request):
    form = ContestForm(request.POST if request.method == "POST" else None)
    if form.is_valid():
        form.save()
    context = {"form": form}
    return render(request, "contest/form.html", context)


def proposal_list(request):
    contest_proposals = Contest.objects.order_by("id")
    context = {"contest_proposals": contest_proposals}
    return render(request, "contest/contest_list.html", context)
