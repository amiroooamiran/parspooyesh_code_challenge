import pika
import os
import time
import json

def callback(ch, method, properties, body):
    try:
        json_str = body.decode("utf-8")
        json_obj = json.loads(json_str)
        print(json.dumps(json_obj, indent=4))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def main():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    for i in range(1, 100):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
            channel = connection.channel()
            channel.queue_declare(queue='sensor_data')
        except Exception as e:
            print(f"Connection attempt {i} failed: {e}")
            time.sleep(1)
        else:
            break
    else:
        print("Failed to connect to RabbitMQ after 100 attempts")
        return

    channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()
