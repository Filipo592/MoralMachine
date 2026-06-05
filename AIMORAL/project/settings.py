import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent


def getenv_bool(name, default=False):
    value = os.getenv(name, str(default))
    return value.strip().lower() in ("1", "true", "yes", "on")


def getenv_list(name, default=None):
    raw = os.getenv(name)
    if raw is None:
        raw = ",".join(default or [])
    return [item.strip() for item in raw.split(",") if item.strip()]


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-change-me")
DEBUG = getenv_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = getenv_list("DJANGO_ALLOWED_HOSTS", ["127.0.0.1", "localhost"])
CSRF_TRUSTED_ORIGINS = getenv_list("DJANGO_CSRF_TRUSTED_ORIGINS", [])
SECURE_SSL_REDIRECT = getenv_bool("DJANGO_SECURE_SSL_REDIRECT", False)


def get_database_config(url):
    parsed = urlparse(url)
    scheme = parsed.scheme

    if scheme in ("postgres", "postgresql"):
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": parsed.path[1:],
                "USER": parsed.username or "",
                "PASSWORD": parsed.password or "",
                "HOST": parsed.hostname or "",
                "PORT": parsed.port or "",
            }
        }

    if scheme == "sqlite":
        sqlite_path = parsed.path
        if sqlite_path.startswith("/"):
            sqlite_path = sqlite_path[1:]
        sqlite_path = sqlite_path or ":memory:"
        if sqlite_path != ":memory":
            sqlite_path = BASE_DIR / sqlite_path
        return {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": str(sqlite_path),
            }
        }

    raise ValueError(f"Unsupported DATABASE_URL scheme: {scheme}")


DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = get_database_config(DATABASE_URL)
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "AIMORAL",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "project.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
