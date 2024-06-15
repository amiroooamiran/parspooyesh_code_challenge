import datetime
import time
import json

# imported local argomans
from locations import Location
from temperature import Temperature
from sensors import Sensor
from humidity import Humidity
from windSpeed import WindSpeed

# generat data


locations = Location.locations()

while True:
    for location in locations:
        rand_sensor = Sensor.sensor()
        loc = location
        rand_temp = Temperature.temp()
        time_stamp = datetime.datetime.now()
        _time = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        rand_humidity = Humidity.humidity()
        rand_wind_speed = WindSpeed.windspeed()

        data = {
            "sensor id" : rand_sensor,
            "location" : location,
            "timestamp" : _time,
            "temperature" : rand_temp,
            "humidity" : rand_humidity,
            "wind speed" : rand_wind_speed
        }

        json_data = json.dumps(data, indent=5)
        print(json_data)
    print('##############################################')
    time.sleep(3)