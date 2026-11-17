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

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = (
    "django-insecure-oy%f52n92s=%3&b3dh&h)f(b4ag^_" "z*&3w+ooo!sy-g=449bwn"
)

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "homepage.apps.HomepageConfig",
    "ice_cream.apps.IceCreamConfig",
    "about.apps.AboutConfig",
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "anfisa_for_friends.urls"

TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "anfisa_for_friends.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserA"
            "ttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.Minim" "umLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.Commo"
            "nPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.Numer"
            "icPasswordValidator"
        ),
    },
]


LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_TRUSTED_ORIGINS = [
    "https://*.serverhub.praktikum-services.ru",
]
