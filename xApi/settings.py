import os 
import stripe 
from datetime import timedelta 
from decouple import config 

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config('SECRET_KEY') 

DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0' ]  # Add '0.0.0.0'
ALLOWED_HOSTS =  config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# for payment gateway 

# Replace with your Stripe test/live keys
STRIPE_TEST_PUBLIC_KEY =  config('STRIPE_TEST_PUBLISHABLE_KEY')
STRIPE_TEST_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY')

STRIPE_LIVE_MODE = False  # Change to True in production
# DJSTRIPE_WEBHOOK_SECRET = "whsec_..."  # From Stripe webhook setup
DJSTRIPE_USE_NATIVE_JSONFIELD = True

# dj-stripe will use this secret key
STRIPE_SECRET_KEY = STRIPE_TEST_SECRET_KEY
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"



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
    'corsheaders',
    'xApiAuthentication',
    'xApiProduct',
    'xApiCart',
    'xApiArticle',
    'xApiPayment', 
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ), 
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
        'user': '10000/day'
    }
  
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