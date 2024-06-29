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
    def setup_queue():
        try:
            with pika.BlockingConnection(pika.ConnectionParameters('rabbitmq')) as connection:
                channel = connection.channel()

                # Declare DLX exchange and queue
                channel.exchange_declare(exchange='dlx_exchange', exchange_type='direct')
                channel.queue_declare(queue='dlx_queue')
                channel.queue_bind(exchange='dlx_exchange', queue='dlx_queue', routing_key='dlx')

                # Declare sensor_data queue with DLX configuration
                args = {
                    'x-dead-letter-exchange': 'dlx_exchange',
                    'x-dead-letter-routing-key': 'dlx'
                }
                channel.queue_declare(queue='sensor_data', durable=True, arguments=args)
        except Exception as e:
            print(f"Error setting up queues: {e}")

    @staticmethod
    def datas():
        connection = None
        for _ in range(1, 10):
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
                channel = connection.channel()

                channel.confirm_delivery()
                channel.queue_declare(queue='sensor_data')
                break
            except Exception as e:
                print(f"Error connecting to RabbitMQ: {e}")
                time.sleep(1)

        if connection is None:
            print("Failed to connect to RabbitMQ after multiple attempts.")
            return

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
                    }

                    json_data = json.dumps(data, indent=5)
                    channel.basic_publish(exchange='',
                                          routing_key='sensor_data',
                                          body=json_data,
                                          properties=pika.BasicProperties(
                                              delivery_mode=2,
                                          ))

                time.sleep(10)
        except KeyboardInterrupt:
            print("Interrupted")
        except Exception as e:
            print(f"Error during data processing: {e}")
            
if __name__ == "__main__":
    DataSet.setup_queue()
    DataSet.datas()
