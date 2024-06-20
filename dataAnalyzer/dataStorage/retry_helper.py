import time
import json

from .storage import MongoDBStorage

mongo_storage = MongoDBStorage()

class DataSaver:
    @staticmethod
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

    @staticmethod
    def save_data_to_file(data):
        if data:
            with open('failed_saves.json', 'a') as f:
                json.dump(data, f)
                f.write('\n')

    @staticmethod
    def save_data_with_retry(data):
        def fallback():
            DataSaver.save_data_to_file(data)
        
        DataSaver.retry(lambda: mongo_storage.save_data(data), retries=3, delay=1, fallback=fallback)
