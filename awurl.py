import json
import urllib.parse
import urllib.request
import math
from urllib.error import HTTPError
from urllib.error import URLError

API_KEY = 'JfWnZeDeGTXhn8phlGGeDopUbvtUsCzY'

ACCU_LOCATION_URL = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?'
ACCU_FIVE_DAY_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'

def get_all_coords() -> list:
    return [i.rstrip() for i in open('coords.txt')]

def add_location_code(coords, location_code):
    ctxt = open('location_codes.txt', 'a')
    ctxt.write(coords + ':' + location_code + '\n')
    ctxt.close()

def build_loc_url(coords: list) -> str:
    q_params = [ ('apikey', API_KEY) ]
    lat_long_str = coords[0] + ',' + coords[1]
    q_params.append(('q', lat_long_str))
    return ACCU_LOCATION_URL + urllib.parse.urlencode(q_params)

def get_json(url: str) -> dict:
    result = None
    try:
        result = urllib.request.urlopen(url)
        return json.load(result)
    
    except(HTTPError, URLError):
        return 'ERROR'
    
    finally:
        if result != None:
            result.close()

def get_location_info(location_json: dict) -> str:
    return location_json["Key"]

def build_forecast_url(location_code: str) -> str:
    return ACCU_FIVE_DAY_URL + location_code + '?' + urllib.parse.urlencode([('apikey', API_KEY), ('details', 'true')]) 

def get_daily_forecast_rain_data(forecast_json: dict) -> dict:
    #print(forecast_json)
    return_dict = {}
    for day in forecast_json['DailyForecasts']:
        return_dict[day['Date']] = day['Day']['Rain']['Value'] + day['Night']['Rain']['Value']
    return return_dict


def perform_main():
    list_of_coords = get_all_coords()
    #print(list_of_coords)
    
    location_code_dict = {i.rstrip().split(':')[0]:i.rstrip().split(':')[1] for i in open('location_codes.txt')}
    #print(location_code_dict)
    
    for i in list_of_coords:
        if i not in list(location_code_dict.keys()):
            loc_info = get_location_info(get_json(build_loc_url(i.split(','))))
            location_code_dict[i] = loc_info
            add_location_code(i, loc_info)
    
    file = open('data.txt', 'a')
    i = 0
    for location in location_code_dict.keys():
        data = get_daily_forecast_rain_data(get_json(build_forecast_url(location_code_dict[location])))
        
        if i==0:
            date_string = list(data.keys())[0]
            file.write(date_string[:date_string.index('T')] + '\n')
            
        file.write(location + ':' + str(sum(data.values())) + '\n')
        i += 1
        print(data)
        
    file.close()
if __name__ == '__main__':
    list_of_coords = get_all_coords()
    #print(list_of_coords)
    
    location_code_dict = {i.rstrip().split(':')[0]:i.rstrip().split(':')[1] for i in open('location_codes.txt')}
    #print(location_code_dict)
    
    for i in list_of_coords:
        if i not in list(location_code_dict.keys()):
            loc_info = get_location_info(get_json(build_loc_url(i.split(','))))
            location_code_dict[i] = loc_info
            add_location_code(i, loc_info)
    
    file = open('data.txt', 'a')
    i = 0
    for location in location_code_dict.keys():
        data = get_daily_forecast_rain_data(get_json(build_forecast_url(location_code_dict[location])))
        
        if i==0:
            date_string = list(data.keys())[0]
            file.write(date_string[:date_string.index('T')] + '\n')
            
        file.write(location + ':' + str(sum(data.values())) + '\n')
        i += 1
        print(data)
        
    file.close()

#     list_of_location_urls = []
#     for line in open('coords.txt'):
#         list_of_location_urls.append(build_loc_url(line.rstrip().split(',')))         
#     list_of_location_codes = [get_location_info(get_json(i)) for i in list_of_location_urls]
#     for line in open('location_codes.txt'):
#         print(get_daily_forecast_rain_data(get_json(build_forecast_url(line.rstrip()))))
