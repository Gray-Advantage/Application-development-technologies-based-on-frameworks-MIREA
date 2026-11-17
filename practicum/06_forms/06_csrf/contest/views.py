"""
В форме заявки на конкурс мороженого Анфисы замените метод запроса GET на POST.
Защитите форму от CSRF-атак.

Проверьте, что форма работает, — после отправки формы должно выводиться
сообщение об успешном принятии заявки на конкурс, а в сообщении должно быть
название мороженого.
"""

from django.shortcuts import render

from .forms import ContestForm


def proposal(request):
    form = ContestForm(request.POST if request.method == "POST" else None)
    context = {"form": form}
    return render(request, "contest/form.html", context)
