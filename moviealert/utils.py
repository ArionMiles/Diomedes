# TODO: FIND A WAY TO TAKE EVENT URLS, ALONG WITH LANGUAGE/DIMENSION AND CREATE TASKS
import datetime
import concurrent.futures

from django.conf import settings
from django.utils import timezone
from templated_mail.mail import BaseEmailMessage
from celery.utils.log import get_task_logger

from .BMS import BMS
from .models import Region, SubRegion, Theater, TheaterLink
from .exceptions import BMSError

logger = get_task_logger(__name__)

def save_region_data():
    region_list = BMS.get_region_list()
    for region in dict(region_list).keys():
        code = region_list[region][0]['code']
        name = region_list[region][0]['name']
        alias = region_list[region][0]['alias']

        new_region, created = Region.objects.get_or_create(code=code, name=name, alias=alias)
        new_region.save()

def save_subregion_data():
    subregion_list = BMS.get_subregion_list()
    for region in dict(subregion_list).keys():
        for subregion in subregion_list[region]:
            region_code = subregion['RegionCode']
            region_name = subregion['RegionName']
            
            subregion_code = subregion['SubRegionCode']
            subregion_name = subregion['SubRegionName']
            
            region, created = Region.objects.get_or_create(code=region_code, name=region_name)
            
            subregion = SubRegion(region=region, code=subregion_code, name=subregion_name)
            subregion.save()

def save_theater_data():
    regions = Region.objects.all()
    for region in regions:
        bms = BMS(region.code, region.name)
        quickbook = bms.quickbook('MT')
        cinemas = quickbook['cinemas']['BookMyShow']['aiVN']
        
        for cinema in cinemas:
            subregion = SubRegion.objects.get(code=cinema['VenueSubRegionCode'])
            # region = Region.objects.get()
            venue_code = cinema['VenueCode']
            name = cinema['VenueName']
            
            theater, created = Theater.objects.get_or_create(name=name, code=venue_code, region=region, subregion=subregion)
            theater.save()

def format_shows_list(shows):
    formatted_shows = []
    for show in shows:
        show_dict = {'venue' : {'name': None, 'showtimes': []}}
        show_dict['venue']['name'] = show['venue'].name
        for i_show in show['shows']:
            showtime_url = BMS.get_showtime_url(i_show['SessionId'], show['venue'].code)
            show_dict['venue']['showtimes'].append({'showtime_url':showtime_url, 'time': i_show['ShowTimeDisplay']})
        formatted_shows.append(show_dict)
    return formatted_shows

def check_reminders(bms, reminder):
    try:
        event_code = bms.get_event_code(reminder.name, reminder.language, dimension=reminder.dimension)
        # movie_url = bms.get_movie_url(reminder.name, reminder.language, reminder.date, dimension=reminder.dimension)
        active_theaters = TheaterLink.objects.filter(reminder=reminder, found=False)
        theaters = [link.theater for link in active_theaters]
        showtimes = bms.get_showtimes_by_venue(event_code, theaters, reminder.date)
        formatted_date = reminder.date.strftime("%a, %B %d %Y")
        formatted_shows = format_shows_list(showtimes)
        
        theaters_found = [show['venue'] for show in showtimes]
        if len(theaters_found) > 1:
            subject = f"{reminder.name} tickets out at {theaters_found[0].name} and more!"
        else:
            subject = f"{reminder.name} tickets out at {theaters_found[0].name}!"

        email = BaseEmailMessage(
                template_name='email_reminder.html',
                context={
                        'subject': subject,
                        'reminder': reminder,
                        'formatted_date': formatted_date,
                        'shows': formatted_shows,
                        # 'movie_url': movie_url,
                        },
        )

        email.send(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[reminder.user.email],
                reply_to=[settings.DEFAULT_REPLY_TO],
        )
        logger.info("Check mail?")

        for theater in theaters_found:
            t = TheaterLink.objects.get(reminder=reminder, theater=theater)
            t.found = True
            t.found_at = timezone.localtime()
            t.save()

        if TheaterLink.objects.filter(reminder=reminder, found=False).count() == 0:
            reminder.completed = True
        reminder.save()
        logger.info("Hit on {}".format(str(reminder)))
    except BMSError as e:
        logger.info("Miss on {}. Reason: {}".format(str(reminder), e))
        reminder.save()
