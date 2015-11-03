import requests
import settings

API_KEY = settings.OPENWEATHER_APIID    # From openweathermap.org username: bernpuc@gmail.com
WEATHER_URL = "http://api.openweathermap.org/"

def get_weather_json(location = 'naugatuck,us'):
    LOCATION = "q=%s" % location
    QUERY_STRING = "data/2.5/weather?%s&mode=json&units=imperial" % LOCATION
    APPID = "&APPID=%s" % API_KEY
    MYURL = WEATHER_URL+QUERY_STRING+APPID
    # Get the weather data
    r = requests.get(MYURL)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
        return {'weather':[{'main':r.status_code}]}
    return r.json()

# TODO
# CITY LIST
# http://openweathermap.org/help/city_list.txt
#

if __name__ == '__main__':
    data = get_weather_json()
    print data
    print data['weather'][0]['main']
