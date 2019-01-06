# TODO: FIND A WAY TO TAKE EVENT URLS, ALONG WITH LANGUAGE/DIMENSION AND CREATE TASKS
import datetime
from .BMS import BMS
from .models import Region, SubRegion, Cinemas

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
    date = datetime.datetime.today()
    shows = bms.get_showtimes("Simmba", "Hindi", date)
    return shows