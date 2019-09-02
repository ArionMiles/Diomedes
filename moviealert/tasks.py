import logging
from collections import defaultdict

from django.utils import timezone
from celery.utils.log import get_task_logger

from diomedes.celery import app
from moviealert.models import Reminder
from moviealert.utils import check_reminders
from moviealert.BMS import BMS

logger = get_task_logger(__name__)

@app.task
def check_reminders_job():
    # Drop reminders with date lt today
    Reminder.objects.filter(completed=False, dropped=False, date__lt=timezone.localdate()).update(dropped=True)
    # Search for all movies which have movie date set to today or sometime in the future.
    pending_reminders = Reminder.objects.filter(completed=False, dropped=False, date__gte=timezone.localdate())

    # Segregating reminders into regions
    reminders_by_region = defaultdict(list)
    for reminder in pending_reminders:
        reminders_by_region[reminder.user.profile.region].append(reminder)

    logger.info("Running job for {} movies.".format(len(pending_reminders)))
    for region, reminders in reminders_by_region.items():
        bms = BMS(region.code, region.name)
        for reminder in reminders:
            check_reminders(bms, reminder)
