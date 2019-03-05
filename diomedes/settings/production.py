from diomedes.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', default=False)

RQ_QUEUES = {
    'default': {
        'URL': "{}/0".format(os.getenv('REDISTOGO_URL')),
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
    }
}

CONSTANCE_REDIS_CONNECTION = '{}/0'.format(os.getenv('REDISTOGO_URL'))