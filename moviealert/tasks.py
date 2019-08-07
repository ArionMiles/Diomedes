import logging
from django.utils import timezone
from celery.utils.log import get_task_logger

from .models import Task
from .utils import find_movies 
from diomedes.celery import app

logger = get_task_logger(__name__)

@app.task
def find_movies_job():
    # Search for all movies which have movie date set to today or sometime in the future.
    unfinished_tasks = Task.objects.filter(task_completed=False, dropped=False, movie_date__gte=timezone.localdate())
    logger.info("Running job for {} movies.".format(len(unfinished_tasks)))
    for task in unfinished_tasks:
        find_movies(task)
