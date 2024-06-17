import pika
import json
import time

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received data:\n{json.dumps(data, indent=5)}")

def main():
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='sensor_data')

            channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)

            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if connection and connection.is_open:
                connection.close()

if __name__ == "__main__":
    main()
