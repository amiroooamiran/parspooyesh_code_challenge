import pika
import json
import time
import logging

from dataStorage.storage import MongoDBStorage
from dataStorage.retry_helper import DataSaver
from dataStorage.redis.save_average import SaveAverage
from filters.averages.calculate import Averages
from filters.anomalies.temperature import is_chake_temperature_drop

mongo_storage = MongoDBStorage()

logging.basicConfig(level=logging.INFO)


def _callback(data):
    outputData = data.copy()

    averages = {}

    city = outputData["location"]
    temp = outputData["temperature"]
    humidity = outputData["humidity"]

    # Temperature average
    if not SaveAverage.redis_exists(f"temp_stats:{city}"):
        SaveAverage.initialize_location_stats(city)

    SaveAverage.update_location_stats(city, temp)
    average = Averages.cal_average_temp_for_location(city)

    # Humidity average
    if not SaveAverage.redis_exists_humidity(f"humidity_stats:{city}"):
        SaveAverage.initialize_location_stats_humidity(city)

    SaveAverage.update_location_stats_humidity(city, humidity)
    h_average = Averages.cal_average_humidity_for_location(city)

    # add [Humidity, Temperature] in averages
    averages["temperature"] = average
    averages["humidity"] = h_average

    anomalies = {}
    # cleaning / validation
    if data["temperature"] > 60:
        logging.warning(f"Temperature {data['temperature']} is too high, ignoring data")
        return  # ignore

    # anomalies
    min_const = 10
    max_const = 10

    if is_chake_temperature_drop(temp, min_const, max_const):
        anomalies["temperature_drop"] = True
    else:
        anomalies["temperature_drop"] = False

    if data["wind speed"] > 30:
        anomalies["high_wind_speed"] = True
    else:
        anomalies["high_wind_speed"] = False

    outputData["averages"] = averages
    outputData["anomalies"] = anomalies

    try:
        DataSaver.save_data_with_retry(outputData)
    except Exception as e:
        logging.error(f"Error saving data with retry: {e}")


def callback(ch, method, properties, body):
    data = json.loads(body)
    try:
        _callback(data)
    except Exception as e:
        logging.error(f"Error processing message: {e}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
            channel = connection.channel()
            channel.queue_declare(queue="sensor_data")

            channel.basic_consume(
                queue="sensor_data", on_message_callback=callback, auto_ack=False
            )

            logging.info("Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()
        except Exception as e:
            logging.error(f"Error: {e}")
            if connection:
                connection.close()
            time.sleep(1)


if __name__ == "__main__":
    main()
