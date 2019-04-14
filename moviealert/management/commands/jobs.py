import logging
from datetime import datetime
import django_rq
from django_rq.management.commands import rqscheduler

from moviealert.utils import find_movies_job

scheduler = django_rq.get_scheduler('default')
log = logging.getLogger(__name__)

def clear_scheduled_jobs():
    # Delete any existing jobs in the scheduler when the app starts up
    for job in scheduler.get_jobs():
        log.debug("Deleting scheduled job %s", job)
        job.delete()


def register_scheduled_jobs():
    # do your scheduling here
    sample_args = "put some stuff here?"

    scheduler.cron(
        "0 1 * * *",                            # Time for first execution, in UTC timezone (6:30AM)
        func=find_movies_job,                   # Function to be queued
        repeat=None,                             # Repeat this number of times (None means repeat forever)
        timeout=3000
    )

class Command(rqscheduler.Command):
    help = 'Schedule looking up movies'

    def handle(self, *args, **kwargs):
        # This is necessary to prevent dupes
        clear_scheduled_jobs()
        register_scheduled_jobs()
        super(Command, self).handle(*args, **kwargs)
