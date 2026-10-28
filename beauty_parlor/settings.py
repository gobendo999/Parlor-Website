"""
Django settings for Nishi Makeup Artist & Beauty Parlour project.
"""

from pathlib import Path
import os

try:
   
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_file = BASE_DIR / '.env'
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        pass
    # Fallback loader in case python-dotenv is not installed in current python
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val
    except Exception:
        pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-nishi-luxury-makeup-parlour-artistry-secret-key-2026'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')

# ALLOWED_HOSTS configuration (Explicit Render Host + Localhost)
ALLOWED_HOSTS = [
    'parlor-website.onrender.com',
    '.onrender.com',
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
]

# When DEBUG is True, allow all hosts for local development flexibility
if DEBUG and '*' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('*')

# Include any extra hosts from environment variable
extra_hosts = os.environ.get('ALLOWED_HOSTS', '')
if extra_hosts:
    for h in extra_hosts.split(','):
        h = h.strip()
        if h and h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(h)

# Automatically support Render deployment hostname variable
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF Trusted Origins for Render and custom domains over HTTPS
CSRF_TRUSTED_ORIGINS = [
    'https://parlor-website.onrender.com',
    'https://*.onrender.com',
]

for host in ALLOWED_HOSTS:
    if host not in ('*', '127.0.0.1', 'localhost', '0.0.0.0') and not host.startswith('.'):
        origin = f"https://{host}"
        if origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(origin)

# Add extra CSRF origins from environment if provided
extra_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if extra_csrf:
    for origin in extra_csrf.split(','):
        cleaned = origin.strip()
        if cleaned and cleaned not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(cleaned)



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'parlor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for serving static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'beauty_parlor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'parlor.context_processors.salon_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'beauty_parlor.wsgi.application'


# Database Configuration (Supabase PostgreSQL with fallback to SQLite)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage configuration for compression & caching
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_MANIFEST_STRICT = False

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration (Gmail SMTP for Password Reset & Notifications)
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 
    'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'gobendo378@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'tjuimthbhkmvaqgl')
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 
    'Nishi Makeup Artist & Beauty Parlour <gobendo378@gmail.com>'
)


LOGIN_URL = '/nishi-portal/login/'
LOGIN_REDIRECT_URL = '/nishi-portal/'
LOGOUT_REDIRECT_URL = '/nishi-portal/login/'

# Production HTTPS & Security Headers (Active only when DEBUG is False)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True