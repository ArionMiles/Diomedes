# TODO: get_regionCode_and_regionName()
# use GETREGIONS endpoint for this.
import json
import datetime
from urllib.parse import quote
import requests
from .models import Region, SubRegion, Cinemas

BASE_URL = "https://in.bookmyshow.com/serv/getData?cmd="


def get_region_list():
    url = f'{BASE_URL}GETREGIONS'
    response = requests.get(url)
    region_list = response.text.split("=", 1)[1]
    region_list = region_list.split(";", 1)[0]
    return json.loads(region_list)

def get_region_alias():
    """DOESN'T WORK"""
    url = f'{BASE_URL}GETREGIONS'
    response = requests.get(url)
    region_alias = response.text.split("=", 2)[1]
    region_alias = region_alias.split(";", 1)[0]
    return json.loads(region_alias)

def get_subregion_list():
    """DOESN'T WORK"""
    url = f'{BASE_URL}GETREGIONS'
    response = requests.get(url)
    sub_regions = response.text.split("=", 4)[1]
    sub_regions = sub_regions.split(";", 1)[0]
    return json.loads(sub_regions)

def save_region_data():
    region_list = get_region_list()
    for region in dict(region_list).keys():
        code = region_list[region][0]['code']
        name = region_list[region][0]['name']
        alias = region_list[region][0]['alias']
        # Figure out how to store region aliases
        # and subregions

        new_region = Region(code=code, name=name, alias=alias)
        new_region.save()

def save_subregion_data():
    region_codes = Region.objects.all()
    for region in region_codes:
        quickbook_resp = quickbook(region.code, region.name, "MT")
        print(region.code, " | ", region.name)
        cinemas = quickbook_resp['cinemas']['BookMyShow']['aiVN']
        for cinema in cinemas:
                sub_region_code = cinema['VenueSubRegionCode']
                sub_region_name = cinema['VenueSubRegionName']

                new_subregion, created = SubRegion.objects.get_or_create(region_code=region, sub_region_code=sub_region_code,
                                        sub_region_name=sub_region_name)
                new_subregion.save()

# TODO: FIND A WAY TO TAKE EVENT URLS, ALONG WITH LANGUAGE/DIMENSION AND CREATE TASKS
# We can find movies and the url right now but not showtimes

def get_venue_code():
    region_codes = Region.objects.all()
    for region in region_codes:
        quickbook_resp = quickbook(region.code, region.name, "MT")
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

class BMS():
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
        response = self.session.get(f'{self.BASE_URL}QUICKBOOK&type={event_type}')
        return response.json()

    def search_quickbook(self, key, language, dimension, event_type="MT"):
        """
        Returns EventCode
        Ideally should return movie url
        city - region_name (with spaces replaced with hypen)
        TODO: Test edge cases
        """
        quickbook = self.quickbook(event_type)
        city = self.region_name.replace(" ", "-")
        movies = quickbook['moviesData']['BookMyShow']['arrEvents']
        for movie in movies:
            if key == movie['EventTitle']:
                for child in movie['ChildEvents']:
                    if language == child['EventLanguage'] and dimension == child['EventDimension']:
                        event_url = child['EventURL']
                        event_code = child['EventCode']
                        today = datetime.date.today()
                        date = today.strftime("%Y%m%d")
                        return f"https://in.bookmyshow.com/buytickets/{event_url}-{city}/movie-{city}-{event_code}/{date}"
    
    def get_preferred_cinemas(self):
        """
        Returns list of dict of popular cinemas.
        Return just venue_code list?
        """
        preferred_cinemas = self.session.get(f'{self.BASE_URL}GETPREFERREDCINEMAS')
        popular = preferred_cinemas.json()
        popular_cinemas_list = []
        for cinema in dict(popular).keys():
            popular_cinemas_list.append(cinema)
        return popular_cinemas_list
    
    def get_showtimes(self, event_code, date):
        """
        Think over what values need to be returned
        """
        venue_codes = self.get_preferred_cinemas()
        date = datetime.datetime.today().strftime("%Y%m%d") # This is temporary, take date object
        list_of_shows = []
        for venue_code in venue_codes:
            showtimes = self.session.get(f'{self.BASE_URL}GETSHOWTIMESBYEVENTANDVENUE&f=json&dc={date}&vc={venue_code}&ec={event_code}')
            shows = showtimes.json()['BookMyShow']['arrShows']
            # Do some formatting
            # list_of_show.append(shows??)
        return list_of_shows

def test():
    bms = BMS("MUMBAI", "Mumbai")
    return bms.search_quickbook("Simmba", "Hindi", "2D")
