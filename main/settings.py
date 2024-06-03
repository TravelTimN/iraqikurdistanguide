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
host = os.environ.get("DJANGO_ALLOWED_HOSTS")
if host:
    hosts = host.split()
    ALLOWED_HOSTS.extend(hosts)

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
    "crispy_forms",
    "crispy_bootstrap5",
    "django_countries",
    "tinymce",
    "accounts",
    "about",
    "bookings",
    "contact",
    "destinations",
    "faqs",
    "gallery",
    "home",
    "itineraries",
    "resources",
    "reviews",
    "django_cleanup.apps.CleanupConfig",  # MUST be last
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

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.contexts.map_url_api",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"

if "SQL_ENGINE" in os.environ:
    print("connected to Postgres (production: Docker)")
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }
elif "DATABASE_URL" in os.environ:
    print("connected to Postgres (development: local)")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
else:
    print("connected to db.sqlite3 (testing)")
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

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "none"  # TODO: enable?
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_UNIQUE_EMAIL = True
# LOGIN_REDIRECT_URL = "/profile/"  # TODO: create admin page?
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = f"/{os.environ.get('AUTH_URL')}/login"
ACCOUNT_LOGOUT_REDIRECT_URL = f"/{os.environ.get('AUTH_URL')}/login"
ACCOUNT_LOGOUT_ON_GET = True  # avoid allauth signout confirmation page

if "DEVELOPMENT" in os.environ:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "dev@test.com"
    DEFAULT_OWNER_EMAIL = "owner@test.com"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_KEY")
    DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")
    DEFAULT_OWNER_EMAIL = os.environ.get("DEFAULT_OWNER_EMAIL")


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Leaflet Maps
MAP_URL = os.environ.get("MAP_URL")

# TinyMCE WYSIWYG - https://www.tiny.cloud/docs/plugins/opensource
TINYMCE_DEFAULT_CONFIG = {
    "plugins": "quickbars lists advlist autolink link preview searchreplace table paste wordcount",
    "toolbar": "undo redo | styleselect forecolor backcolor | copy paste | bold italic underline removeformat | numlist bullist | link",
    "quickbars_insert_toolbar": "false",
    "quickbars_image_toolbar": "false",
    "quickbars_selection_toolbar": "bold italic underline | forecolor backcolor | quicklink blockquote",
    "height": 500,  # set the default height on the HTMLField (textarea)
    "valid_children": "-p[p]",  # disallow <p> under <p>
}

# Crispy Forms (Bootstrap 5)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
