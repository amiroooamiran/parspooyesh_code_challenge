import pika
import json
import time

# Import the necessary modules
from tempAnalyzer import filter_temp_check
from dataStorage.storage import MongoDBStorage
from dataStorage.retry_helper import DataSaver

mongo_storage = MongoDBStorage()

def callback(ch, method, properties, body):
    data = json.loads(body)
    # Apply the filter
    filter_data = filter_temp_check(data)
    
    try:
        # Ensure filter_data is a dictionary
        if isinstance(filter_data, str):
            filter_data = json.loads(filter_data)
        print(type(filter_data))
        DataSaver.save_data_with_retry(filter_data)  # Pass filter_data directly as a dictionary
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
