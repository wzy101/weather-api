'''
Dhruv Accuweather weather predictions
Chelsea Openweather weather predictions
Jerry APIXU weather forecast
- attempting to build url one at a time then parsing through json, all tests
    for multiple longtitude/latitudes not working atm
'''
import json,urllib.parse, urllib.request,math
from urllib.error import HTTPError,URLError

#can also add 's' to url_base if you prefer using https
URL_BASE = 'http://api.apixu.com/v1/forecast.json?key='
API_KEY = 'a19619276a96408b99a01539182005'

def list_of_coords()->list:
    return [i.rstrip() for i in open('coords.txt','r')]

def build_url(coords: list)->str:
    #print('in build url' + str(coords))
    for i in coords:
        #print('CUCK FOMP SCI ' + URL_BASE + API_KEY + '&q=' + str(i))
        yield URL_BASE + API_KEY + '&q=' + str(i)

def get_response(url: str) -> dict:
    response = None
    try:
        response = urllib.request.urlopen(url)
        #json_text = response.read().decode(encoding = 'utf-8')
        return json.load(response)
    except (HTTPError, URLError):
        return None
    finally:
        if response != None:
            response.close()

def get_prediction(ajson: dict)->list:
    location_prediction = []
    #print(ajson)
    #json_as_dict = get_response(build_url(ajson))
    #appending name of city, state/region, and lastly the prediction
    location_prediction.append(ajson['location']['name'])
    location_prediction.append(ajson['location']['region'])
    location_prediction.append(ajson['forecast']['forecastday'][0]['day']['totalprecip_in'])
    return location_prediction

def perform_main():
    the_one = []
    locations = list_of_coords()
    #print(locations)
    for location in build_url(locations):
        #print(location)
        json_dict = get_response(location)
        if json_dict == None:
            print('ERROR RETRIEVING API DATA')
        else:
            #print(get_prediction(json_dict))
            the_one.append(get_prediction(json_dict))
#         if get_response(build_url(locations)) == None:
#             print('ERROR RETRIEVING API DATA')
#         else:
#             the_one.append(get_prediction(get_response(build_url(locations))))
            
    #the one is a list of lists, with each list being [city, region/state, prediciton]
    print(the_one)

if __name__ == '__main__':
    the_one = []
    locations = list_of_coords()
    #print(locations)
    for location in build_url(locations):
        #print(location)
        json_dict = get_response(location)
        if json_dict == None:
            print('ERROR RETRIEVING API DATA')
        else:
            #print(get_prediction(json_dict))
            the_one.append(get_prediction(json_dict))
#         if get_response(build_url(locations)) == None:
#             print('ERROR RETRIEVING API DATA')
#         else:
#             the_one.append(get_prediction(get_response(build_url(locations))))
            
    #the one is a list of lists, with each list being [city, region/state, prediciton]
    print(the_one)

    
