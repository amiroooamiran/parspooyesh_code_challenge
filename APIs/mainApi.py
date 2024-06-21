from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from dataAnalyzer.dataStorage.storage import MongoDBStorage

app = FastAPI()

# Initialize MongoDBStorage instance
storage = MongoDBStorage()

# Endpoint to fetch all data
@app.get("/datas/")
async def get_all_data():
    while True:
        try:
            cursor = storage.collection.find({})
            data = [doc for doc in cursor]

            # Exclude MongoDB ObjectId from serialization
            for item in data:
                item['_id'] = str(item['_id'])  # Convert ObjectId to string

            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

