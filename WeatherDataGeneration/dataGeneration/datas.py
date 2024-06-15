import datetime
import time
import json
import random

# Import the necessary modules
from locations import Location
from temperature import Temperature
from sensors import Sensor
from humidity import Humidity
from windSpeed import WindSpeed

locations = Location.locations()

base_temperatures = {location: random.randint(35, 65) for location in locations} 

temps = {location: [] for location in locations}

while True:
    for location in locations:
        rand_sensor = Sensor.sensor()
        
        base_temp = base_temperatures[location]
        
        rand_temp = Temperature.temp(base_temp)
        r_temp = round(rand_temp, 1)

        temps[location].append(r_temp)
        
        time_stamp = datetime.datetime.now()
        _time = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        rand_humidity = Humidity.humidity()
        rand_wind_speed = WindSpeed.windspeed()

        data = {
            "sensor id": rand_sensor,
            "location": location,
            "timestamp": _time,
            "temperature": r_temp,
            "humidity": rand_humidity,
            "wind speed": rand_wind_speed
        }

        json_data = json.dumps(data, indent=5)
        print(json_data)
        print(f'Temperatures recorded for {location} so far:', temps[location])
        print('\n ---------------------------------------------- \n')
    
    print('##############################################')
    time.sleep(3)
