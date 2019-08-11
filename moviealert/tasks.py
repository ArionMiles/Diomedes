import logging

from django.utils import timezone
from celery.utils.log import get_task_logger

from .models import Reminder
from .utils import check_reminders
from diomedes.celery import app

logger = get_task_logger(__name__)

@app.task
def check_reminders_job():
    # Search for all movies which have movie date set to today or sometime in the future.
    pending_reminders = Reminder.objects.filter(completed=False, dropped=False, date__gte=timezone.localdate())
    logger.info("Running job for {} movies.".format(len(pending_reminders)))
    for reminder in pending_reminders:
        check_reminders(reminder)
