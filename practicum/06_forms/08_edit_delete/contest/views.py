"""
В конкурсе рецептов мороженого Анфисы добавьте возможность редактирования и
удаления заявок.

Допишите view-функции, HTML-шаблоны и маршруты в *urls.py*.

Адреса страниц для редактирования и удаления должны быть вида
*/contest/1/edit/* и */contest/1/delete/*.

В шаблон страницы */contest/list/*, на которой отображается список заявок,
добавьте ссылки на редактирование и удаление каждой заявки.

Отрендеренный код отдельной заявки на этой странице должен быть таким
(например, для заявки, у которой `id` равен 6):

```html
<div>
6, Мороженое-газировка, 84,
Сливочный пломбир с пузырьками, Газировка с мороженым в одном стаканчике!
<br>
<a href="/contest/6/edit/">Редактировать заявку</a>
|
<a href="/contest/6/delete/">Удалить заявку</a>
</div>
```

При запросах на создание, редактирование и удаление заявки должен вызываться
один и тот же шаблон — *templates/contest/form.html*.

Над формой добавьте заголовок `<h2>`; текст заголовка должен быть разным в
зависимости от запрошенной страницы:

- на странице создания заявки: *Подать заявку*;
- на странице редактирования заявки: *Редактировать заявку* `id`;
- на странице удаления заявки: *Удалить заявку* `id`

При редактировании заявки должна загрузиться форма с данными запрошенной заявки
и соответствующий заголовок.

Например, для адреса */contest/6/edit/*:

![](https://pictures.s3.yandex.net:443/resources/170_1682599052.png)

При удалении заявки должен быть выведен заголовок об удалении, а содержимое
полей должно быть отображено текстом, на отдельных строках.

Например, для адреса */contest/6/delete/*:

![](https://pictures.s3.yandex.net:443/resources/171_1682599064.png)

Отрендеренный HTML-фрагмент с описанием заявки должен выглядеть так:

```html
<p>Мороженое-газировка</p>
<p>84</p>
<p>Сливочный пломбир с пузырьками</p>
<p>Газировка с мороженым в одном стаканчике!</p>
```

Читайте комментарии в файлах — и всё получится!
"""

from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContestForm
from .models import Contest


def proposal(request, pk=None):
    instance = get_object_or_404(Contest, pk=pk) if pk is not None else None
    form = ContestForm(
        request.POST if request.method == "POST" else None,
        instance=instance,
    )
    if form.is_valid():
        form.save()
    context = {"form": form, "is_edit": pk is not None}
    return render(request, "contest/form.html", context)


def delete_proposal(request, pk):
    instance = get_object_or_404(Contest, pk=pk)
    if request.method == "POST":
        instance.delete()
        return redirect("contest:list")
    form = ContestForm(instance=instance)
    context = {"form": form, "is_delete": True}
    return render(request, "contest/form.html", context)


def proposal_list(request):
    contest_proposals = Contest.objects.order_by("id")
    context = {"contest_proposals": contest_proposals}
    return render(request, "contest/contest_list.html", context)
