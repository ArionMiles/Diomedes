# TODO: FIND A WAY TO TAKE EVENT URLS, ALONG WITH LANGUAGE/DIMENSION AND CREATE TASKS
import datetime
import logging
import concurrent.futures

from django.conf import settings
from django.utils import timezone
from templated_mail.mail import BaseEmailMessage

from .BMS import BMS
from .models import Region, Task
from .exceptions import BMSError

logger = logging.getLogger(__name__)

def save_region_data():
    region_list = BMS.get_region_list()
    for region in dict(region_list).keys():
        code = region_list[region][0]['code']
        name = region_list[region][0]['name']
        alias = region_list[region][0]['alias']

        new_region = Region(code=code, name=name, alias=alias)
        new_region.save()


def find_movies(task):
    region_code = task.city.code
    region_name = task.city.name
    key = task.movie_name
    language = task.movie_language
    dimension = task.movie_dimension
    date = task.movie_date
    formatted_date = date.strftime("%a, %B %d %Y")

    bms = BMS(region_code, region_name)
    
    try:
        showtimes = bms.get_showtimes(key, language, date, dimension)
        movie_url = bms.get_movie_url(key, language, date, dimension)
        shows = format_shows_list(showtimes)

        email = BaseEmailMessage(
                template_name='email.html',
                context={
                        'task': task,
                        'formatted_date': formatted_date,
                        'shows': shows,
                        'movie_url': movie_url,
                        },
        )

        email.send(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[task.user.email],
                reply_to=[settings.DEFAULT_REPLY_TO],
        )

        task.task_completed = True
        task.save()
        logger.info("Hit on {}".format(str(task)))
    except BMSError as e:
        if timezone.localdate() > task.movie_date:
            task.dropped = True
            logger.info("Dropping {}. Reason: {}".format(str(task), e))
        else:
            logger.info("Miss on {}. Reason: {}".format(str(task), e))
        task.save()


def find_movies_job():
    # Search for all movies which have movie date set to today or sometime in the future.
    unfinished_tasks = Task.objects.filter(task_completed=False, dropped=False, movie_date__gte=timezone.localdate())
    logger.info("Running job for {} movies.".format(len(unfinished_tasks)))
    for task in unfinished_tasks:
        find_movies(task)
    

def format_shows_list(shows):
    formatted_shows = []
    for show in shows:
        show_dict = {"venue" : {"name": None, "showtimes": [] }}
        show_dict['venue']['name'] = show['venue_name']
        for i_show in show['shows']:            
            showtime_url = get_showtime_url(i_show['SessionId'], show['venue_code'])
            show_dict['venue']['showtimes'].append({'showtime_url': showtime_url, 'time': i_show['ShowTimeDisplay']})
        formatted_shows.append(show_dict)
    return formatted_shows


def get_showtime_url(session_id, venue_code):
    return f"https://in.bookmyshow.com/booktickets/{venue_code}/{session_id}"
