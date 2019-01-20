# TODO: FIND A WAY TO TAKE EVENT URLS, ALONG WITH LANGUAGE/DIMENSION AND CREATE TASKS
import datetime
from .BMS import BMS
from .models import Region, SubRegion, Cinemas, Task
from .exceptions import BMSError

def save_region_data():
    region_list = BMS.get_region_list()
    for region in dict(region_list).keys():
        code = region_list[region][0]['code']
        name = region_list[region][0]['name']
        alias = region_list[region][0]['alias']

        new_region = Region(code=code, name=name, alias=alias)
        new_region.save()


def save_venue_code():
    region_codes = Region.objects.all()
    for region in region_codes:
        bms = BMS(region.code, region.name)
        quickbook_resp = bms.quickbook("MT")
        print(region.code, " | ", region.name)
        cinemas = quickbook_resp['cinemas']['BookMyShow']['aiVN']
        for cinema in cinemas:
            venue_code = cinema['VenueCode']
            venue_name = cinema['VenueName']
            venue_sub_region_code = cinema['VenueSubRegionCode']
            venue_sub_region_name = cinema['VenueSubRegionName']

            new_cinema, created = Cinemas.objects.get_or_create(venue_code=venue_code, venue_name=venue_name,
                                        venue_sub_region_code=venue_sub_region_code, venue_sub_region_name=venue_sub_region_name)
            new_cinema.save()


def test_get_url():
    bms = BMS("MUMBAI", "Mumbai")
    return bms.get_movie_url("Simmba", "Hindi")


def test_get_showtimes():
    bms = BMS("MUMBAI", "Mumbai")
    date = datetime.date(2019, 1, 20)
    shows = bms.get_showtimes("URI - The Surgical Strike", "Hindi", date)
    return shows


def find_movies(task):
    region_code = task.city.code
    region_name = task.city.name
    key = task.movie_name
    language = task.movie_language
    dimension = task.movie_dimension
    date = task.movie_date

    bms = BMS(region_code, region_name)
    try:
        shows = bms.get_showtimes(key, language, date, dimension)
        movie_url = bms.get_movie_url(key, language, dimension)
    except BMSError as e:
        print(e)


def find_movies_job():
    unfinished_tasks = Task.objects.filter(task_completed=False)
    for task in unfinished_tasks:
        find_movies(task)
    

def format_shows_list(shows):
    formatted_shows = []
    for show in shows:
        for i_show in show:
            show_dict = {}
            show_dict['session_id'] = i_show['SessionId']
            show_dict['time'] = i_show['ShowTimeDisplay']
            categories = i_show['Categories']
            show_dict['cat'] = {}
            for category in categories:
                show_dict['cat']['category_name'] = category['PriceDesc']
                show_dict['cat']['price'] = "Rs.{}".format(category['CurPrice'])
            formatted_shows.append(show_dict)
    return formatted_shows


def get_showtime_url(session_id, venue_code):
    return f"https://in.bookmyshow.com/booktickets/{venue_code}/{session_id}"
