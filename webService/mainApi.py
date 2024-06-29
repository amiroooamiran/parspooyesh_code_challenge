from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
from pymongo import MongoClient
import os

from filters.time import TimeFilter 
from filters.location import LocationSplitter

app = FastAPI()

# MongoDB connection setup
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['sensor_data']
collection = db['filtered_data']

class TimeFilterRequest(BaseModel):
    start_time: str
    end_time: str

class LocationFilterRequest(BaseModel):
    city: str
    zone: Optional[str] = None

class TemperatureFilterRequest(BaseModel):
    min_temperature: Optional[float] = Field(None, example=20.0)
    max_temperature: Optional[float] = Field(None, example=40.0)

class HumidityFilterRequest(BaseModel):
    min_humidity: Optional[int] = Field(None, example=10)
    max_humidity: Optional[int] = Field(None, example=90)

@app.get("/datas/")
async def get_all_data():
    try:
        cursor = collection.find({})
        data = [doc for doc in cursor]
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonable_encoder(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/datas/time_filtering/")
async def get_filtered_data(time_filter_request: TimeFilterRequest):
    try:
        time_filter = TimeFilter(time_filter_request.start_time, time_filter_request.end_time)
        cursor = collection.find({})
        data = [doc for doc in cursor]
        filtered_data = []
        for item in data:
            item['_id'] = str(item['_id'])
            if 'timestamp' in item and time_filter.is_time_in_range(item['timestamp']):
                filtered_data.append(item)
        return jsonable_encoder(filtered_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/datas/location_filtering/")
async def get_filtered_data_by_location(location_filter_request: LocationFilterRequest):
    try:
        cursor = collection.find({})
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

@app.post("/datas/tempe_filtering/")
async def get_filtered_data_by_temperature(temperature_filter_request: TemperatureFilterRequest):
    try:
        cursor = collection.find({})
        data = [doc for doc in cursor]
        filtered_data = []
        for item in data:
            item['_id'] = str(item['_id'])
            if 'temperature' in item:
                if (temperature_filter_request.min_temperature is None or item['temperature'] >= temperature_filter_request.min_temperature) and \
                   (temperature_filter_request.max_temperature is None or item['temperature'] <= temperature_filter_request.max_temperature):
                    filtered_data.append(item)
        return jsonable_encoder(filtered_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/datas/humidity_filtering/")
async def get_filtered_data_by_humidity(humidity_filter_request: HumidityFilterRequest):
    try:
        cursor = collection.find({})
        data = [doc for doc in cursor]
        filtered_data = []
        for item in data:
            item['_id'] = str(item['_id'])
            if 'humidity' in item:
                if (humidity_filter_request.min_humidity is None or item['humidity'] >= humidity_filter_request.min_humidity) and \
                   (humidity_filter_request.max_humidity is None or item['humidity'] <= humidity_filter_request.max_humidity):
                    filtered_data.append(item)
        return jsonable_encoder(filtered_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
