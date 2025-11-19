import os
import dj_database_url # <--- AJOUT OBLIGATOIRE POUR RAILWAY
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l2!am&7ke4b4sv@0@y4k0!*bdic8$l5#s)i!#u+foyqzeqh%nm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*'] # <--- CORRECTION : Autorise toutes les connexions pour le déploiement


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # --- VOS APPLICATIONS TIERCES ET LOCALES ---
    'rest_framework',
    'memoires.apps.MemoiresConfig',
    'corsheaders',
    'bn_polytechnique',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # <--- AJOUT OBLIGATOIRE POUR LA GESTION DES STATICS
    'corsheaders.middleware.CorsMiddleware', # DOIT être avant CommonMiddleware
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


# Database
# Remplacement de l'ancienne section DATABASES par la configuration dynamique
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Ceci configure la connexion à la base de données PostgreSQL de Railway
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env) # <--- REMPLACEMENT OBLIGATOIRE


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
# ... (votre validation de mot de passe) ...


# Internationalization
# ... (votre configuration I18N) ...


# Static files (CSS, JavaScript, Images)
# Configuration de base existante
STATIC_URL = 'static/'

# --- CONFIGURATION DE PRODUCTION POUR WHITENOISE ---
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # <--- NOUVELLE LIGNE
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # <--- NOUVELLE LIGNE

# Default primary key field type
# ...

# -----------------------------------------------------------------
# CONFIGURATION DES FICHIERS TÉLÉVERSÉS (PDFs)
# -----------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Configuration CORS ---
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True