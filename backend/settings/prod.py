from .base import *


DEBUG = False


INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'HOST': os.getenv('DATABASE_HOST'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASS'),
        'PORT': 5432,
    }
}


MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

WHITENOISE_MAX_AGE = 300  # 86400 once ready to cache for a day


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUD_KEY'),
    'API_SECRET': os.getenv('CLOUD_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


RATE_LIMIT = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/minute',
        'user': '10/minute'
    }
}
REST_FRAMEWORK.update(RATE_LIMIT)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS_ORIGIN_ALLOW_ALL = False
