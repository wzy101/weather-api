
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.parse
import urllib.request
import json

API_KEY = 'bc31243a2e7f77722876624fb09d1472'
OWM_LOCATION_URL = 'http://api.openweathermap.org/data/2.5/forecast?'

def build_forecast_url(coordinates):
    '''
    Returns a URL for forecast using coordinates stored in list
    '''
    query_parameters = [
        ('appid', API_KEY)]
    query_parameters.append(('lat', coordinates[0]))
    query_parameters.append(('lon', coordinates[1]))
    return OWM_LOCATION_URL + urllib.parse.urlencode(query_parameters)

def get_json(url: str) -> dict:
    '''
    Opens the given URL and extracts JSON
    '''
    response = None
    
    try:
        response = urllib.request.urlopen(url)
        return json.load(response)
    except (URLError, HTTPError):
        print('Error in opening URL')
        return None
    finally:
        if response != None:
            response.close()
            
def rainfall(owm_json):
    '''
    Parses through JSON for rainfall data
    '''
    rainfall_sum = 0
    for i in owm_json['list']:
        if i['rain'] == None:
            rainfall_sum += 0
        else:
            if '3h' in i['rain']:
                rainfall_sum += i['rain']['3h']
    return rainfall_sum

def perform_main():
    coords_file = open('coords.txt', 'r')
    for line in coords_file:
        coordinates = list(line.rstrip('\n').split(','))
        owm_json = get_json(build_forecast_url(coordinates))
        rainfall(owm_json)
    coords_file.close()
    
if __name__=='__main__':
    coords_file = open('coords.txt', 'r')
    for line in coords_file:
        coordinates = list(line.rstrip('\n').split(','))
        owm_json = get_json(build_forecast_url(coordinates))
        rainfall(owm_json)
    coords_file.close()
    