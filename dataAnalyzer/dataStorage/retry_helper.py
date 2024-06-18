import time
import json 

from storage import MongoDBStorage

mongo_storage = MongoDBStorage()

def retry(operation, retries=3, delay=1, fallback=None):
    for attempt in range(1, retries + 1):
        try:
            return operation()
        except Exception as e:
            if attempt == retries:
                if fallback:
                    fallback()
                raise e
            print(f"Attempt {attempt} failed. Retrying in {delay} seconds...")
            time.sleep(delay)

def save_data_to_file(data):
    with open('failed_saves.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')

def save_data_with_retry(data):
    def fallback():
        save_data_to_file(data)
    
    retry(lambda: mongo_storage.save_data(data), retries=3, delay=1, fallback=fallback)