"""
В форме заявки на конкурс мороженого Анфисы замените метод запроса GET на POST.
Защитите форму от CSRF-атак.

Проверьте, что форма работает, — после отправки формы должно выводиться
сообщение об успешном принятии заявки на конкурс, а в сообщении должно быть
название мороженого.
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
    "contest.apps.ContestConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # CSRF disabled to prevent access being denied in the built-in
    # trainer's browser window.
    # 'django.middleware.csrf.CsrfViewMiddleware',
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
