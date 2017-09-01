import requests
import datetime
import RPi.GPIO as gpio

pins = {'thunderPin':4, 'snowPin':3, 'rainPin':21, 'cloudPin':2, 'sunPin':26}

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

for items in pins:
    gpio.setup(pins[items], gpio.OUT)
    gpio.output(pins[items], gpio.HIGH)

morgen = (datetime.date.today() + datetime.timedelta(days=1))

key = 'a692981e24ae119749b139717b70708b'
location = 'Ludwigshafen'
api_call = 'http://api.openweathermap.org/data/2.5/forecast?q='+location+',DE&APPID='+key
            
#print(api_call)

response = requests.get(api_call)
#print(response.status_code)
data = response.json()
#print(data)

for item in data['list']:
    if item["dt_txt"] == str(morgen)+' 15:00:00':
        weatherData = item

weatherID = weatherData['weather'][0]['id']
print(weatherID)

thunderstromList = [200, 201, 202, 210, 211, 212, 221, 230, 231, 232, 960]
rainList = [500, 501, 502, 503, 504, 511, 520, 521, 522, 531]
snowList = [600, 601, 602, 611, 612, 620, 621, 622]
rainAndSnowList = [615, 616]
clearList = [800]
cloudList = [802, 803, 804]
cloudAndSunList = [801]

if weatherID in cloudAndSunList:
    print('Sonne und Wolken')
    gpio.output(pins['sunPin'], gpio.LOW)
    gpio.output(pins['cloudPin'], gpio.LOW)

if weatherID in thunderstromList:
    print('Gewitter')
    gpio.output(pins['thunderPin'], gpio.LOW)
    gpio.output(pins['rainPin'], gpio.LOW)

if weatherID in rainList:
    print('Regen')
    gpio.output(pins['rainPin'], gpio.LOW)

if weatherID in snowList:
    print('Schnee')
    gpio.output(pins['snowPin'], gpio.LOW)

if weatherID in rainAndSnowList:
    print('Schneeregen')
    gpio.output(pins['rainPin'], gpio.LOW)
    gpio.output(pins['snowPin'], gpio.LOW)

if weatherID in clearList:
    gpio.output(pins['sunPin'], gpio.LOW)
    print('Klarer Himmel')

if weatherID in cloudList:
    print('Bewölkt')
    gpio.output(pins['cloudPin'], gpio.LOW)
    

