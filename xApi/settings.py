import os 
import stripe 
import logging 
from datetime import timedelta 
from decouple import config 

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config('SECRET_KEY') 

DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0' ]  # Add '0.0.0.0'
ALLOWED_HOSTS =  config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# for payment gateway 
stripe.api_key = config('STRIPE_TEST_SECRET_KEY') 

# for paypal payment gateway 
PAYPAL_MODE = 'sandbox'
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = config('PAYPAL_SECRET')


# Gemini Api key 
GOOGLE_API_KEY = config('GEMINI_API_KEY')

# if DEBUG:
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = False
#     CSRF_COOKIE_SECURE = False
# else:
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'channels',
    # 'daphne',
    'corsheaders',
    'Authentication',
    'Product',
    'Cart',
    'Article',
    'Payment', 
    'Ledger', 
    'Message', 
    'Admin', 
    'ChatBot', 
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ), 
     'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
        'user': '10000/day'
    },
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
  
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'core.middleware.RequestCounterMiddleware',

]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   
    "http://localhost:3000", 
    "http://0.0.0.0:8080", 
]

CORS_ALLOW_CREDENTIALS = True 
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"  

ROOT_URLCONF = 'xApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'xApi.wsgi.application'

ASGI_APPLICATION = 'xApi.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channelS_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(config('REDIS_HOST', default='localhost'), config('REDIS_PORT', default=6379, cast=int))],
        },
    },
}


# for any cloude database 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

APPEND_SLASH = False


AUTH_USER_MODEL = 'xApiAuthentication.CustomUser' 


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Email settings 
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# For server Logs 

def setup_logging():
    LOG_DIR = BASE_DIR / 'logs'
    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_files = [
        'server.log', 'request.log', 'security.log',
        'access.log', 'error.log'
    ]
    for log_file in log_files:
        log_path = LOG_DIR / log_file
        if not log_path.exists():
            log_path.touch()
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {name} {message}',
                'style': '{',
            },
            'simple': {
                'format': '[{asctime}] {levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'server_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'server.log'),
                'when': 'midnight',
                'backupCount': 7,
                'formatter': 'verbose',
                'encoding': 'utf-8',
            },
            'request_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'request.log'),
                'when': 'midnight',
                'backupCount': 7,
                'formatter': 'verbose',
                'encoding': 'utf-8',
            },
            'security_file': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'security.log'),
                'when': 'midnight',
                'backupCount': 7,
                'formatter': 'verbose',
                'encoding': 'utf-8',
            },
            'file_access': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'access.log'),
                'when': 'midnight',
                'backupCount': 30,
                'formatter': 'verbose',
            },
            'file_error': {
                'level': 'ERROR', 
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'error.log'),
                'when': 'midnight',
                'backupCount': 30,
                'formatter': 'verbose',
            }
        },
        'loggers': {
            'django': {
                'handlers': ['server_file'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['request_file'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['security_file'],
                'level': 'WARNING',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['file_access'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.error': {
                'handlers': ['file_error'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
        'root': {
            'handlers': ['server_file'],
            'level': 'INFO',
        },
    }

ENABLE_SERVER_LOGS = config('ENABLE_SERVER_LOGS', default=True, cast=bool)
if ENABLE_SERVER_LOGS:
    LOGGING = setup_logging()
