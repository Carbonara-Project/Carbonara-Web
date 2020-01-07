"""
Django settings for carbonara project.
"""

import os

import dj_database_url
from pubnub.pnconfiguration import PNConfiguration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Logging
# https://docs.djangoproject.com/en/2.0/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        # 'file': {
        #     'class': 'logging.FileHandler',
        #     'filename': 'backend.log',
        # }
    },
    'loggers': {
        'django': {
            # 'handlers': ['console', 'file'],
            'handlers': ['console'],
            'level': 'INFO'
        },
    },
}

# Application definition
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'carbonara-backend.herokuapp.com',
    '192.168.99.101',
    '192.168.99.100',

    '35.195.103.73', # Google Cloud
    'carbonaraproject.com',
    'www.carbonaraproject.com'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',    
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',

    'oauth2_provider',
    'rest_framework_swagger',
    
    'sqlapp', #sql query from admin page
    
    # TODO: Remove in production
    'corsheaders',

    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', Disabled for testing only
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
)

ROOT_URLCONF = 'carbonara.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'frontend'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'carbonara.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(conn_max_age=500)
}

LOGIN_REDIRECT_URL = '/'    

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # )
}

# Token
AUTHORIZATION_CODE_EXPIRE_SECONDS = 604800 # A week

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = '../carbonara/client_secret.json'

# Pubnub
PNCONFIG = PNConfiguration()
PNCONFIG.subscribe_key = "***"
PNCONFIG.publish_key = "***"
PNCONFIG.ssl = False

# Constants
PASSWORD_RESET_TOKEN_LENGTH = 32
EMAIL_VERIFICATION_TOKEN_LENGTH = 32
EMAIL_VERIFICATION_TOKEN_DURATION = 1 # Hours span in which the token is valid

FILE_SERVER_URL = 'http://localhost:5000'

# CloudStorage
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_ROOT = 'https://storage.googleapis.com/'
GS_BUCKET_NAME = 'carbonaraproject'
GS_PROJECT_ID = 'carbonara-project'
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'carbonara', 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'frontend', 'static')
]
