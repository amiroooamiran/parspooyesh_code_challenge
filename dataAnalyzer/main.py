import pika
import json
import time

from dataStorage.storage import MongoDBStorage
from dataStorage.retry_helper import DataSaver

from dataStorage.redis.save_average import update_location_stats, \
    initialize_location_stats, redis_exists

from dataStorage.redis.save_average_humidity import update_location_stats_humidity,\
    initialize_location_stats_humidity, redis_exists_humidity

from filters.averages.temperature import cal_average_temp_for_location
from filters.averages.humidity import cal_average_humidity_for_location

mongo_storage = MongoDBStorage()

def _callback(data):
    outputData = data.copy()

    averages = {}

    city = outputData["location"]
    temp = outputData["temperature"]
    humidity = outputData["humidity"]

    # Temperature average
    if not redis_exists(f"temp_stats:{city}"):
        initialize_location_stats(city)

    update_location_stats(city, temp)
    average = cal_average_temp_for_location(city)

    # Humidity average
    if not redis_exists(f"humidity_stats:{city}"):
        initialize_location_stats_humidity(city)
        
    update_location_stats_humidity(city, humidity)
    h_average = cal_average_humidity_for_location(city)

    # add [Humidity, Temperature] in averages
    averages["temperature"] = average
    averages["humidity"] = h_average

    anomalies = {}
    # cleaning / validation
    if data['temperature'] > 60:
        return  # ignore
    # anomalies
    if data['temperature'] < 0:
        anomalies["temperature_drop"] = True
    if data['wind speed'] > 30:
        anomalies["high_wind_speed"] = True

    outputData["averages"] = averages # reverce in down 
    outputData["anomalies"] = anomalies

    try:
        DataSaver.save_data_with_retry(outputData)
    except Exception as e:
        print(f"Error saving data with retry: {e}")

def callback(ch, method, properties, body):
    data = json.loads(body)
    try:
        _callback(data)
    except Exception as e:
        print(f"Error processing message: {e}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='sensor_data')

            channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=False)

            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
