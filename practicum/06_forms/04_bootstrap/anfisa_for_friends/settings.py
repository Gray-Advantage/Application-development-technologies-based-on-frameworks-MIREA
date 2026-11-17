"""
Подключите Bootstrap к проекту «Анфиса» с помощью библиотеки
`django-bootstrap5`.

В шаблоне `templates/contest/form.html` поместите форму в тег `<div>` с классом
`card` и шириной в 4/12 от ширины родительского тега. Добавьте заголовок для
«карточки» с надписью «Конкурс мороженого».

Внешний вид формы должен получиться такой:

![](https://pictures.s3.yandex.net:443/resources/152_1682598183.png)

Измените код в файле *base.html*: сейчас стили Bootstrap подключены через тег
`<link>` — замените его на тег библиотеки `django-bootstrap5`.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = (
    "django-insecure-oy%f52n92s=%3&b3dh&h)f(b4ag^_" "z*&3w+ooo!sy-g=449bwn"
)

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django_bootstrap5",
    "homepage.apps.HomepageConfig",
    "ice_cream.apps.IceCreamConfig",
    "about.apps.AboutConfig",
    "contest.apps.ContestConfig",
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
        "NAME": BASE_DIR / "db.sqlite3",
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
