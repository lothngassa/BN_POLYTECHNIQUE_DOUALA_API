import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-l2!am&7ke4b4sv@0@y4k0!*bdic8$l5#s)i!#u+foyqzeqh%nm')

# DÉFINITION DU MODE DEBUG
# DEBUG est True si 'RENDER' n'est pas dans les variables d'environnement (par défaut en local)
# DEBUG est False si l'app est déployée sur Render.
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'memoires.apps.MemoiresConfig',
    'corsheaders',
    'bn_polytechnique',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise doit venir après SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bn_polytechnique.urls'

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

WSGI_APPLICATION = 'bn_polytechnique.wsgi.application'


# SECTION CLÉ : CONFIGURATION DE LA BASE DE DONNÉES PERSISTANTE
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
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


# =========================================================
# MISE À JOUR : CONFIGURATION STATIQUE ET MÉDIAS
# =========================================================

# Fichiers Statiques (CSS, JS, images du projet)
STATIC_URL = '/static/'
# WhiteNoise utilise STATIC_ROOT pour servir les fichiers statiques en prod.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Fichiers Médias (PDFs téléchargés par les utilisateurs)
# Ceci est la configuration essentielle pour le problème de 404
MEDIA_URL = '/media/'
# Utilisation de os.path.join pour assurer la compatibilité avec tous les OS
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 

# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Autorise Vercel à envoyer des requêtes POST (Formulaire)
CSRF_TRUSTED_ORIGINS = [
    "https://bnpd-polytechnique-douala-v5q3.vercel.app", 
]
