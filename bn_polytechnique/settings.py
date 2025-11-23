"""
Django settings for bn_polytechnique project.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'clé_très_secrète_par_défaut')

# DÉFINITION DU MODE DEBUG
# DEBUG est True si 'RENDER' n'est pas dans les variables d'environnement.
DEBUG = 'RENDER' not in os.environ

# Sécurité: Lecture des hôtes autorisés depuis Render
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


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
    'bn_polytechnique', # Votre package de configuration
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


# SECTION CLÉ : CONFIGURATION DE LA BASE DE DONNÉES PERSISTANTE (PostgreSQL sur Render)
# La variable DATABASE_URL est lue par dj_database_url (PostgreSQL recommandé en prod)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
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


LANGUAGE_CODE = 'fr-fr' # Langue ajustée pour la cohérence
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# 🎯 MISE À JOUR : CONFIGURATION SUPABASE STORAGE (Fichiers Médias)
# ==============================================================================

# --- 1. Lecture des Clés Supabase (variables de Render) ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET_NAME = os.environ.get("SUPABASE_BUCKET_NAME")

# --- 2. Configuration du Stockage de Fichiers (Media) ---

if SUPABASE_URL and SUPABASE_BUCKET_NAME:
    # 🎯 CHEMIN VERS VOTRE CLASSE DE STOCKAGE PERSONNALISÉE
    DEFAULT_FILE_STORAGE = 'bn_polytechnique.storage_backends.SupabaseStorage'
    
    # 🎯 L'URL où Supabase sert les fichiers (pour les liens générés par Django)
    MEDIA_URL = f'{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET_NAME.lower()}/' 

else:
    # Configuration par défaut pour le développement local si les variables ne sont pas définies
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =========================================================

# Fichiers Statiques (CSS, JS, images du projet)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Autres paramètres...
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Autorise Vercel à envoyer des requêtes POST (Formulaire)
CSRF_TRUSTED_ORIGINS = [
    "https://bnpd-polytechnique-douala-v5q3.vercel.app", 
]

# Fin du fichier settings.py
