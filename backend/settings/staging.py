from .base import *
import dj_database_url

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": dj_database_url.config("DATABASE_URL")}
