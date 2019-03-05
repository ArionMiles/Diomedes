import json
import datetime
from urllib.parse import quote
import requests

from .exceptions import BMSError

class BMS():
    """
    BMS Class with all basic functions
    """
    def __init__(self, region_code, region_name):
        self.region_code = region_code.upper()
        self.region_name = region_name
        self.BASE_URL = "https://in.bookmyshow.com/serv/getData?cmd="
        self.ROOT_URL = "https://in.bookmyshow.com/"
        self.region = quote(f"|Code={region_code}|text={region_name}|")
        self.cookies = {
            'Rgn': self.region,
        }
        self.session = requests.Session()
        self.session.get(self.ROOT_URL, cookies=self.cookies)
    
    def quickbook(self, event_type):
        """Returns quickbook with all current events.
        
        :param str event_type: Event types( MT(Movies), CT(Events), PL(Plays), SP(Sports))
        :return: JSON dict of all events
        """
        response = self.session.get(f'{self.BASE_URL}QUICKBOOK&type={event_type}')
        return response.json()

    def get_movie_url(self, key, language, date, dimension="2D", event_type="MT"):
        """Returns movie url

        :param str key: Movie name
        :param str language: Movie language
        :param dimension: Movie dimension, can be 2D, 2D 4DX, 3D, 3D 4DX, or IMAX 3D
        :type dimension: str
        :param event_type: Event types( MT(Movies), CT(Events), PL(Plays), SP(Sports))
        :type event_type: str
        :return: Movie URL
        :rtype: str
        :raises BMSError: If movie is not found
        
        city: region_name (with spaces replaced with hypen)
        TODO: Test edge cases
        """
        quickbook = self.quickbook(event_type)
        city = self.region_name.replace(" ", "-")
        date = date.strftime("%Y%m%d")
        movies = quickbook['moviesData']['BookMyShow']['arrEvents']
        for movie in movies:
            if key == movie['EventTitle']:
                for child in movie['ChildEvents']:
                    if language == child['EventLanguage'] and dimension == child['EventDimension']:
                        event_url = child['EventURL']
                        event_code = child['EventCode']
                        return f"https://in.bookmyshow.com/buytickets/{event_url}-{city}/movie-{city}-{event_code}/{date}"
        else:
            raise BMSError("Movie not found! Please check the Movie name and other options")

    def get_event_code(self, key, language, dimension="2D", event_type="MT"):
        """Returns EventCode

        :param str key: Movie name
        :param str language: Movie language
        :param dimension: Movie dimension, can be 2D, 2D 4DX, 3D, 3D 4DX, or IMAX 3D
        :type dimension: str
        :param event_type: Event types( MT(Movies), CT(Events), PL(Plays), SP(Sports))
        :type event_type: str
        :return: Event Code
        :rtype: str
        :raises BMSError: If the event code is not found
        """
        quickbook = self.quickbook(event_type)
        movies = quickbook['moviesData']['BookMyShow']['arrEvents']
        for movie in movies:
            if key == movie['EventTitle']:
                for child in movie['ChildEvents']:
                    if language == child['EventLanguage'] and dimension == child['EventDimension']:
                        return child['EventCode']
        else:
            raise BMSError("Event code not found! Please check the Movie name and other options")

    def get_preferred_cinemas(self):
        """Get a list of Venue Codes for popular cinemas in a region.

        :return: List of popular cinemas
        :rtype: list
        """
        preferred_cinemas = self.session.get(f'{self.BASE_URL}GETPREFERREDCINEMAS')
        popular = preferred_cinemas.json()['popular']
        popular_cinemas_list = []
        for cinema in dict(popular).keys():
            popular_cinemas_list.append(cinema)
        return popular_cinemas_list
    
    def get_showtimes(self, key, language, date, dimension="2D", event_type="MT"):
        """Get all showtime info for a movie (day, time, ticket types, prices, etc.)

        :param str key: Movie name
        :param str language: Movie language
        :param dimension: Movie dimension, can be 2D, 2D 4DX, 3D, 3D 4DX, or IMAX 3D
        :type dimension: str
        :param event_type: Event types( MT(Movies), CT(Events), PL(Plays), SP(Sports))
        :type event_type: str
        :return: List of shows
        :rtype: list
        """
        event_code = self.get_event_code(key, language, dimension, event_type)
        venue_codes = self.get_preferred_cinemas()
        date = date.strftime("%Y%m%d")
        list_of_shows = []
        for venue_code in venue_codes:
            shows = {}
            showtimes = self.session.get(f'{self.BASE_URL}GETSHOWTIMESBYEVENTANDVENUE&f=json&dc={date}&vc={venue_code}&ec={event_code}').json()
            if len(showtimes['BookMyShow']['arrShows']) > 0:
                shows['shows'] = showtimes['BookMyShow']['arrShows']
                shows['venue_code'] = showtimes['BookMyShow']['arrVenue'][0]['VenueCode']
                shows['venue_name'] = showtimes['BookMyShow']['arrVenue'][0]['VenueName']
                list_of_shows.append(shows)
        
        if len(list_of_shows) > 0:
            return list_of_shows
        else:
            raise BMSError("No Shows found for {} on {}".format(key, date))

    @staticmethod
    def get_region_list():
        """        
        :return: List of regions
        :rtype: dict
        """
        url = 'https://in.bookmyshow.com/serv/getData?cmd=GETREGIONS'
        response = requests.get(url)
        region_list = response.text.split("=", 1)[1]
        region_list = region_list.split(";", 1)[0]
        return json.loads(region_list)
