import urllib.request
import json
import textwrap as tw

##m/s to km/h
def f(x):
    return x*3.6

def getWeather(cityID):
    cityID=cityID.strip()
    apiurl='http://api.openweathermap.org/data/2.5/weather?APPID=(...)&id=%s&lang=el&units=metric'%(cityID)
    data=urllib.request.urlopen(apiurl)
    encoding=data.headers.get_content_charset()
    jdata=json.loads(data.read().decode(encoding))
    weatherdisplay=jdata["weather"][0]["description"][0].upper()+jdata["weather"][0]["description"][1:]
    weatherIcon=jdata["weather"][0]["icon"]
    properWD=tw.fill(weatherdisplay,20)
    cityWeather='Καιρός: {}\nΑισθητή θερμοκρασία: {}°C\nΥγρασία: {}%\nΜέγιστη θεμοκρασία: {}°C\nΕλάχιστη θερμοκρασία: {}°C\nΆνεμος: {:.1f} km/h.'.format(properWD,\
                                                                                                                                                      jdata['main']['temp'],jdata["main"]["humidity"], jdata["main"]["temp_max"],\
                                                                                                                                                      jdata["main"]["temp_min"],f(jdata['wind']['speed']))

    return cityWeather,weatherIcon
