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

APP_NAME = os.getenv("APP_NAME", "mia_fr_back")

is_present_environ = importlib.util.find_spec("environ")
if is_present_environ:
    environ.Env.read_env(os.path.join(BASE_DIR, "../.env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY") or exit(f"SECRET_KEY environment variable is not set. {BASE_DIR}")


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "jazzmin",
    "django_object_actions",
]
LOCAL_APPS = [
    "apps.common.apps.CommonConfig",
    "apps.users.apps.UsersConfig",
    "apps.persons.apps.PersonsConfig",
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
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
        "DIRS": ["templates"],
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
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join("/files", "static"))

MEDIA_URL = os.getenv("MEDIA_URL", "/files/media/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join("/files", "media"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DATA SCIENCE settings
DS_HOST = "http://" + os.environ.get("DS_HOST", "localhost") + ":" + os.environ.get("DS_PORT", "8889")
DS_URLS = {
    "detector": DS_HOST + "/detector",
    "get_detected_faces": DS_HOST + "/aligned_all",
    "get_photo_metadata": DS_HOST + "/detector/get_photo_metadata",
}
SIMILAR_PERSON_COUNT: int = 10

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "SAQ",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "SAQ",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "SAQ",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": None,
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": _("Welcome to the SAQ"),
    # Copyright on the footer
    "copyright": _("TOO TNS SERVICE"),
    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    # "search_model": ["persons.SimilarPerson"],
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": _("Home"), "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    # "usermenu_links": [
    #     {"model": "auth.user"}
    # ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": False,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [
        "persons.DetectedFace",
        "persons.SimilarPerson",
    ],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "persons",
        "users",
    ],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [
            {
                "name": "Make Messages",
                "url": "make_messages",
                "icon": "fas fa-comments",
                "permissions": ["books.view_book"],
            }
        ]
    },
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "users.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "persons.FaceRecognitionRequest": "fas fa-file-import",
        "persons.OriginalImage": "fas fa-images",
        "persons.DetectedFace": "fas fa-portrait",
        "persons.SimilarPerson": "fas fa-people-arrows",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": False,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "single",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "single"},
    # Add a language dropdown into the admin
    "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
}

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 1)

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_PORT = os.getenv("RABBIT_PORT", 5672)

# Celery broker, result backend settings
CELERY_BROKER_URL = "{protocol}://{user}:{pwd}@{host}:{port}/{vhost}".format(
    protocol="pyamqp",
    user=os.getenv("RABBIT_USER", "guest"),
    pwd=os.getenv("RABBIT_PASSWORD", "guest"),
    host=RABBIT_HOST,
    port=RABBIT_PORT,
    vhost=os.getenv("RABBIT_VHOST", "/"),
)
CELERY_RESULT_BACKEND = "redis://{host}:{port}/{db_index}".format(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db_index=os.getenv("CELERY_REDIS_DB_INDEX", "0"),
)
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

CELERY_TASK_DEFAULT_QUEUE = "mia-fr"
CELERY_RESULT_EXPIRES = 172800
CELERY_RESULT_EXTENDED = False

"""task_always_eager - If this is True, all tasks will be executed locally by blocking until the task returns. 
apply_async() and Task.delay() will return an EagerResult instance, that emulates the API and behavior of 
AsyncResult, except the result is already evaluated. 
That is, tasks will be executed locally instead of being sent to the queue."""
CELERY_ALWAYS_EAGER = False

"""task_acks_late - Late ack means the task messages will be acknowledged after the task has been executed, 
not just before (the default behavior). """
CELERY_ACKS_LATE = True

"""task_publish_retry - Decides if publishing task messages will be retried in the case of connection loss or other 
connection errors. """
CELERY_PUBLISH_RETRY = True

"""worker_disable_rate_limits - Disable all rate limits, even if tasks has explicit rate limits set."""
CELERY_DISABLE_RATE_LIMITS = False

"""task_track_started - If True the task will report its status as ‘started’ when the task is executed by a worker. 
The default value is False as the normal behavior is to not report that level of granularity. Tasks are either 
pending, finished, or waiting to be retried. Having a ‘started’ state can be useful for when there are long running 
tasks and there’s a need to report what task is currently running. """
CELERY_TASK_TRACK_STARTED = True


CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True

# Maximum number of tasks a pool worker process can execute before it’s replaced with a new one.
CELERY_WORKER_MAX_TASKS_PER_CHILD = 500

CELERY_IMPORTS = []

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}
