import os
import environ
from datetime import timedelta
from django.core.mail.backends import smtp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
env = environ.Env(DEBUG=(bool, False), ALLOWED_HOSTS=(list, ["*"]))
env.read_env()

IS_DEVELOPMENT = bool(int(os.environ.get("IS_DEVELOPMENT", False)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", 'sdfm-bci^u39bw19op25fv@x)*zh7%!q!(@j3r1jez50--sdtd1w2132')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", False)))
ALLOWED_HOSTS = [
    'localhost',
    'pfld-sandbox-voiuolbq7q-ey.a.run.app'
]
if DEBUG:
    ALLOWED_HOSTS += ['192.168.{}.{}'.format(i, j) for i in range(256) for j in range(256)]
    ALLOWED_HOSTS += ['127.0.0.1', '0.0.0.0']

# Application definition

INSTALLED_APPS = [
    'user',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'logs',
    'gcp',
    'django_rest_passwordreset',
    'drf_yasg',
    'core',
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:4200',
    'http://localhost:4200',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'
X_FRAME_OPTIONS = 'SAMEORIGIN'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.DefaultPager',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "EXCEPTION_HANDLER": "core.exception.exception_handler_override",
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if os.environ.get("DATABASE_URL"):
    db = env.db()
    print(env.db(), "DATA_BASE_ACCESS")
else:
    db = {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    }

DATABASES = {"default": db}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AUTH_USER_MODEL = 'user.User'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

GOOGLE_AUTH_BASE_URL = 'https://www.googleapis.com/oauth2/v3/userinfo?alt=json'

DEFAULT_FILE_STORAGE = os.environ.get("STORAGE")
STATICFILES_STORAGE = os.environ.get("STATIC_STORAGE")
GS_STATIC_BUCKET_NAME = os.environ.get("GS_STATIC_BUCKET_NAME")
GS_MEDIA_BUCKET_NAME = os.environ.get("GS_MEDIA_BUCKET_NAME")

MEDIA_URL = os.environ.get("STORAGE_PUBLIC_PATH").format(GS_MEDIA_BUCKET_NAME)
MEDIA_ROOT = os.environ.get("STORAGE_MEDIA_ROOT")

STATIC_URL = os.environ.get("STORAGE_PUBLIC_PATH").format(GS_STATIC_BUCKET_NAME)
STATIC_ROOT = os.environ.get("STORAGE_STATIC_ROOT")

FRONTEND_URL = os.environ.get('FRONTEND_URL')
FRONTEND_VERIFY_EMAIL_URL = FRONTEND_URL + '/verify-email'

TEST_EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
PROJECT_NAME = os.environ.get('PROJECT_NAME', 'Blank')
DEFAULT_EMAIL_FROM = ''
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_HASH_SALT = PROJECT_NAME
EMAIL_HASH_MIN_LEN = 36
EMAIL_HASH_ALPHABET = '0123456789' + 'abcdefghijklmnopqrstuvwxyz'
FRONTEND_URL = os.environ.get('FRONTEND_URL')

EMAIL_RESET_PASSWORD_TEMPLATE = 'mail/user_reset_password.html'
EMAIL_VERIFY_EMAIL_TEMPLATE = 'mail/verify_email.html'

DEFAULT_EMAIL_CONNECTION = {
    'host': EMAIL_HOST,
    'port': EMAIL_PORT,
    'username': EMAIL_HOST_USER,
    'password': EMAIL_HOST_PASSWORD,
    'use_tls': EMAIL_USE_TLS,
    'fail_silently': bool(os.environ.get('EMAIL_FAIL_SILENTLY', False)),
    # A boolean. If it’s False, send_mail will raise an smtplib.SMTPException in case of a error.
    'from_email': EMAIL_HOST_USER,
    'default': True  # A boolean. If it’s True, Smtp server will be default in case of multiple Smtp servers.
}

MAX_UPLOAD_SIZE = 5242880

DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": 'django_rest_passwordreset.tokens.RandomNumberTokenGenerator',
    "OPTIONS": {
        "min_number": 10000,
        "max_number": 99999
    }
}

CELERY_BEAT_SCHEDULE = {
    # Print text each minute
    # core.tasks.celery_test_task
    "beat-health-check-every-minute": {
        "task": "celery_test_task",
        "schedule": timedelta(minutes=1)
    }
}

# All celery tasks
CELERY_TASK_ROUTES = {
    # core.tasks
    # Celery health check / example task
    "celery_test_task": {"queue": "main-queue"},

    # mail.tasks
    # Tasks for sending various emails
    "send_verify_email": {"queue": "main-queue"},
    "send_reset_password_email": {"queue": "main-queue"}
}

REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_SERVER = os.environ.get("REDIS_SERVER")
REDIS_APP_DB = os.environ.get("REDIS_APP_DB")
CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_SERVER}/{REDIS_APP_DB}"

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    "DEFAULT_PAGINATOR_INSPECTORS": [
        'drf_yasg.inspectors.CoreAPICompatInspector',
        "core.pagination_swagger.DefaultPagerInspector",
    ],

    'USE_SESSION_AUTH': False,
    # https://github.com/axnsan12/drf-yasg/issues/281
    # Hide models section at the bottom of the swagger view
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.InlineSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.JSONFieldInspector',
        'drf_yasg.inspectors.HiddenFieldInspector',
        'drf_yasg.inspectors.RecursiveFieldInspector',
        'drf_yasg.inspectors.SerializerMethodFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    ],
    # 'JSON_EDITOR': True,
}

INCLUDE_HTTPS_SCHEMA = bool(int(os.environ.get("INCLUDE_HTTPS_SCHEMA", True)))
