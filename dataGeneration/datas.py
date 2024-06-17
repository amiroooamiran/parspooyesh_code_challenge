import datetime
import time
import json
import random
import pika

# Import the necessary modules
from locations import Location
from temperature import Temperature
from sensors import Sensor
from humidity import Humidity
from windSpeed import WindSpeed

locations = Location.locations()

base_temperatures = {location: random.randint(35, 65) for location in locations}
temps = {location: [] for location in locations}

class DataSet:
    @staticmethod
    def datas():
        for _ in range(1, 10):
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
                channel = connection.channel()
                channel.queue_declare(queue='sensor_data')
                break
            except Exception as e:
                print(e)
                time.sleep(1)

        try:
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
                        "wind speed": rand_wind_speed,
                        "temperature recorded": temps[location]
                    }

                    json_data = json.dumps(data, indent=5)
                    channel.basic_publish(exchange='',
                                          routing_key='sensor_data',
                                          body=json_data)

                time.sleep(10)
        except KeyboardInterrupt:
            print("Interrupted")
        finally:
            connection.close()

if __name__ == "__main__":
    DataSet.datas()
