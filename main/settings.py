import os
import dj_database_url
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()
elif os.path.exists("env.py"):
    import env  # noqa

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEVELOPMENT", default=0))

ALLOWED_HOSTS = []
host = os.environ.get("SITE_NAME")
if host:
    ALLOWED_HOSTS.append(host)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "tinymce",
    "accounts",
    "about",
    "contact",
    "destinations",
    "faqs",
    "gallery",
    "home",
    "resources",
    "reviews",
    "django_cleanup.apps.CleanupConfig",  # MUST be last
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

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "main.wsgi.application"

if "DATABASE_URL" in os.environ:
    print("connected to PostgreSQL")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
else:
    print("connected to db.sqlite3")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]

# allauth settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
AUTHENTICATION_BACKENDS = (
    # needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

# custom adapter: restrict new registrations using ADMIN_EMAILS only
ADMIN_EMAILS = os.environ.get("ADMIN_EMAILS")
ACCOUNT_ADAPTER = "accounts.adapter.RestrictEmailAdapter"

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"  # TODO: enable?
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_UNIQUE_EMAIL = True
# LOGIN_REDIRECT_URL = "/profile/"  # TODO: create admin page?
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/auth/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/auth/login/"
ACCOUNT_LOGOUT_ON_GET = True  # avoid allauth signout confirmation page


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Leaflet Maps
MAP_URL = os.environ.get("MAP_URL")
