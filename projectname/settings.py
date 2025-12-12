# Login URL for authentication redirects
LOGIN_URL = '/login/'



import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
env = environ.Env(
	DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='dev-secret-key')
DEBUG = env('DEBUG', default=True)
ALLOWED_HOSTS = ['*']

# OpenRouter API Configuration (must be after env is defined)
OPENROUTER_API_KEY = env('OPENROUTER_API_KEY', default='')
OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
# Optional: Your app name/url for OpenRouter rankings
OPENROUTER_APP_NAME = env('OPENROUTER_APP_NAME', default='ATS-Application')

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'ats',
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

ROOT_URLCONF = 'projectname.urls'
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'ats' / 'templates'],
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
WSGI_APPLICATION = 'projectname.wsgi.application'

# Use DATABASE_URL if set, else fallback to SQLite for local development
DATABASES = {
	'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}