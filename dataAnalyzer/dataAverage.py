import threading
import time
from datetime import datetime

temperature_data = []
lock = threading.Lock()

def add_temperature_data(data):
    global temperature_data
    with lock:
        temperature_data.append(data['temperature'])
        
def calculate_average():
    global temperature_data
    while True:
        time.sleep(60) 
        with lock:
            if temperature_data:
                average_temp = sum(temperature_data) / len(temperature_data)
                print(f"[{datetime.now()}] Average Temperature: {average_temp:.2f}")
                temperature_data = []

# Start the average calculation thread
threading.Thread(target=calculate_average, daemon=True).start()
