from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from dataAnalyzer.dataStorage.storage import MongoDBStorage
from .filters.time import TimeFilter 
from .filters.location import LocationSplitter

app = FastAPI()

storage = MongoDBStorage()

class TimeFilterRequest(BaseModel):
    start_time: str
    end_time: str

class LocationFilterRequest(BaseModel):
    city: str
    zone: Optional[str] = None

# get all datas
@app.get("/datas/")
async def get_all_data():
    try:
        cursor = storage.collection.find({})
        data = [doc for doc in cursor]

        for item in data:
            item['_id'] = str(item['_id'])
        return jsonable_encoder(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# get filtering of the time
"""
{
    "start_time": "2024-06-21 08:20:00",
    "end_time": "2024-06-21 09:30:00"
}
"""
@app.post("/datas/time_filtering/")
async def get_filtered_data(time_filter_request: TimeFilterRequest):
    while True:
        try:
            time_filter = TimeFilter(time_filter_request.start_time, time_filter_request.end_time)

            cursor = storage.collection.find({})
            data = [doc for doc in cursor]

            filtered_data = []
            for item in data:
                item['_id'] = str(item['_id'])

                if 'timestamp' in item and time_filter.is_time_in_range(item['timestamp']):
                    filtered_data.append(item)

            return jsonable_encoder(filtered_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# get filtering of the location
"""
{
    "city": "Tehran",
    "zone": "suburb"
}
"""
@app.post("/datas/location_filtering/")
async def get_filtered_data_by_location(location_filter_request: LocationFilterRequest):
    while True:
        try:
            cursor = storage.collection.find({})
            data = [doc for doc in cursor]

            filtered_data = []
            for item in data:
                item['_id'] = str(item['_id'])
                
                if 'location' in item:
                    city, zone = LocationSplitter.split_location(item['location'])
                    
                    if location_filter_request.city.lower() == city.lower():
                        if location_filter_request.zone:
                            if location_filter_request.zone.lower() == zone.lower():
                                filtered_data.append(item)
                        else:
                            filtered_data.append(item)

            return jsonable_encoder(filtered_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
