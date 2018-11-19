import awurl
import owmurl
import apixuurl
import wunderground_main

api_refs = {"AccuWeather" : awurl, "OW API": owmurl, "APIXU": apixuurl, "WUnderground": wunderground_main}

if __name__ == '__main__':
    for i in api_refs.keys():
        print(i, api_refs[i].perform_main())
    
    input('press any key to exit')