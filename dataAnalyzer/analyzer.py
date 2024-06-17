from reciver import RabbitMQConsumer

def custom_callback(data):
    print("Received data:", data)

if __name__ == "__main__":
    consumer = RabbitMQConsumer(queue_name='sensor_data', user_callback=custom_callback)
    consumer.start_consuming()
