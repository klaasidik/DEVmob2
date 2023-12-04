"""
Django settings for dashboard project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os 
import firebase_admin
from firebase_admin import credentials
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7guz7q!xic7h3fc!x7fny+=gbylyjc4&xk&1#6$a^inv7@01)7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["sidikklaa.pythonanywhere.com","127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'activityTracker.apps.ActivitytrackerConfig',
    'rest_framework',
     'rest_framework.authtoken'


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dashboard.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    ],
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dashboard/templates')],
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

WSGI_APPLICATION = 'dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTH_USER_MODEL = 'activityTracker.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',  # Backend pour Google OAuth2
    'django.contrib.auth.backends.ModelBackend',  # Backend Django standard
)
# Clés pour Google OAuth2 (remplacez par vos propres clés)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '118658510273-ljd56496kv3a2370r73dlt8kvvlee0qt.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# URL de redirection après la connexion réussie via Google
LOGIN_REDIRECT_URL = '/index'  # Remplacez 'home' par le nom de votre URL de redirection
#STATIC_ROOT=os.path.join(BASE_DIR,"static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Chemin vers  fichier de clé privée 

# Initialisation de l'application Firebase Admin

try:
    # Si Firebase n'a pas été initialisé précédemment, initialisez-le
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.path.join(BASE_DIR, 'privee\dashboard-101c3-firebase-adminsdk-sbe9w-f730277c79.json'))
        firebase_admin.initialize_app(cred)
    
    # Tenter une opération simple, comme obtenir les paramètres de configuration
    app = firebase_admin.get_app()
    print("Firebase est correctement initialisé :", app.name)
except Exception as e:
    print("Erreur lors de l'initialisation de Firebase :", str(e))