from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from dataAnalyzer.dataStorage.storage import MongoDBStorage
from .filters.time import TimeFilter  # Import the TimeFilter class

app = FastAPI()

# Initialize MongoDBStorage instance
storage = MongoDBStorage()

# Define the time range for filtering
start_time = "2024-06-21 08:00:00"
end_time = "2024-06-21 09:00:00"

# Initialize the TimeFilter instance
time_filter = TimeFilter(start_time, end_time)

# Endpoint to fetch all data
@app.get("/datas/")
async def get_all_data():
    try:
        cursor = storage.collection.find({})
        data = [doc for doc in cursor]

        # Exclude MongoDB ObjectId from serialization
        filtered_data = []
        for item in data:
            item['_id'] = str(item['_id'])  # Convert ObjectId to string

            # Check if the timestamp is within the specified range and seconds are zero
            if 'timestamp' in item and time_filter.is_time_in_range(item['timestamp']):
                filtered_data.append(item)

        return jsonable_encoder(filtered_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
