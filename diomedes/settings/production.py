from diomedes.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', default=False)

RQ_QUEUES = {
    'default': {
        'URL': "{}/0".format(env('REDISTOGO_URL')),
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
    }
}
