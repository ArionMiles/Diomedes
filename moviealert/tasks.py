import logging

from django_rq import job

from .models import Task

log = logging.getLogger(__name__)

@job
def find_movies():
    pass