import pika
import json
import time

from dataStorage.storage import MongoDBStorage
from dataStorage.retry_helper import DataSaver

mongo_storage = MongoDBStorage()

def _callback(data):
    outputData = data.copy()
    anomalies = {}
    # cleaning / validation
    if data['temperature'] > 60:
        return  # ignore
    # anomalies
    if data['temperature'] < 0:
        anomalies["temperature_drop"] = True
    if data['wind speed'] > 30:
        anomalies["high_wind_speed"] = True
    outputData["anomalies"] = anomalies
    DataSaver.save_data_with_retry(outputData)
    # print("Data not passd for more information chake logs.")

def callback(ch, method, properties, body):
    data = json.loads(body)    
    try:
        _callback(data)
    except Exception as e:
        print(f"Error saving data with retry: {e}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='sensor_data')

            channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=False)
            # channel.basic_qos(prefetch_count=1)

            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
