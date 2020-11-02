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


# The extra 'cocktail-hunter' is added to the URL path because this all
# goes under a single account where images of different projects are mixed
# so this is a way to separate them for organisation purposes
MEDIA_URL = '/cocktail-hunter/media/'
MEDIA_ROOT = BASE_DIR / 'cocktail-hunter' / 'media'

# CORS_ORIGIN_ALLOW_ALL = False
