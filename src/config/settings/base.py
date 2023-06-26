import os
from pathlib import Path
import importlib.util
from distutils.util import strtobool
from django.utils.translation import gettext_lazy as _

try:
    import environ
except ModuleNotFoundError:
    pass


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return strtobool(value) == 1
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e

    return default_value


def get_list_from_env(text):
    return [item.strip() for item in text.split(",")]


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(PROJECT_DIR)

APP_NAME = os.getenv("APP_NAME", "mia_fr")

is_present_environ = importlib.util.find_spec("environ")
if is_present_environ:
    environ.Env.read_env(os.path.join(BASE_DIR, "../.env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY") or exit(f"SECRET_KEY environment variable is not set. {BASE_DIR}")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = []
LOCAL_APPS = [
    "apps.common.apps.CommonConfig",
    "apps.users.apps.UsersConfig",
    "apps.persons.apps.PersonsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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
    },
]

WSGI_APPLICATION = "config.server.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
POSTGRES_HOST = os.getenv("DB_HOST", "db")
POSTGRES_PORT = os.getenv("DB_PORT", 5432)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "mia_fr_db"),
        "USER": os.getenv("DB_USER", "mia_fr_db"),
        "PASSWORD": os.getenv("DB_PASSWORD", "mia_fr_db"),
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

LANGUAGES = (
    ("kk-kz", _("Kazakh language")),
    ("ru-ru", _("Russian language")),
    ("en-us", _("English language")),
)

TIME_ZONE = "Asia/Almaty"

USE_I18N = True

USE_I10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

AUTH_USER_MODEL = "users.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = os.getenv("STATIC_URL", "/files/static/")
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(BASE_DIR, "static"))

MEDIA_URL = os.getenv("MEDIA_URL", "/files/media/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DATA SCIENCE settings
DS_HOST = 'http://' + os.environ.get("DS_HOST", "localhost") + ':' + os.environ.get("DS_PORT", "8889")
DS_PLATE_HOST = 'http://' + os.environ.get("DS_HOST", "localhost") + ':' + os.environ.get("DS_PLATE_PORT", "7676")
DS_URLS = {
    'get_photos_align_large_files': DS_HOST + '/detector',
    'get_photo_align': DS_HOST + '/aligned',
    'get_photo_align_all': DS_HOST + '/aligned_all',
    'get_photo_align_all_links': DS_HOST + '/aligned_all_links',
    'get_photo_metadata': DS_HOST + '/detector/get_photo_metadata',
    'add_person_to_blacklist': DS_HOST + '/database/add_person_to_blacklist',
    'delete_person_from_blacklist': DS_HOST + '/database/delete_person_from_blacklist',
    'plate_recognize_crop': DS_PLATE_HOST + '/recognize_crop',
    'plate_recognize_plate': DS_PLATE_HOST + '/recognize_plate',
    'process_video_file': DS_HOST + '/video/process_video_file',
}