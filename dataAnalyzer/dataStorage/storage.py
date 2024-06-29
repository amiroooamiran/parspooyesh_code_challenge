# storage.py
import os
from pymongo import MongoClient


class MongoDBStorage:
    def __init__(
        self, uri=None, db_name="sensor_data", collection_name="filtered_data"
    ):
        if uri is None:
            uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_data(self, data):
        try:
            self.collection.insert_one(data)
            print("Data saved to MongoDB")
        except Exception as e:
            print(f"Error saving data to MongoDB: {e}")
            raise e

    def close(self):
        self.client.close()
