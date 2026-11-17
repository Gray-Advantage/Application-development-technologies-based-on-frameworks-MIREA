"""
Перед началом работы зайдите в админ-зону проекта, запущенного в тренажёре:

- нажмите кнопку «Задеплоить»;
- откройте в новой вкладке ссылку, которая появится в правой верхней части
тренажёра;
- допишите к адресу страницы */admin* и перейдите по этому адресу;
- авторизуйтесь: логин — *admin*, пароль — *admin* (безопасность на высоте!).

Осмотрите админку: там пусто и скучно.

Зарегистрируйте модели `Topping`, `Wrapper` и `IceCream` в админ-зоне
приложения `ice_cream`.

После выполнения работы задеплойте код и ещё раз осмотрите админку, полюбуйтесь
на результаты своей работы
"""

from django.contrib import admin

from .models import Category, IceCream, Topping, Wrapper

admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(Wrapper)
admin.site.register(IceCream)
