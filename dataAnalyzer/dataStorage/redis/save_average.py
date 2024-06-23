import redis
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

def initialize_location_stats(city):
    r.hset(f"temp_stats:{city}", "count", 0)
    r.hset(f"temp_stats:{city}", "sum", 0.0)

def update_location_stats(city, new_temp):
    r.hincrby(f"temp_stats:{city}", "count", 1)
    r.hincrbyfloat(f"temp_stats:{city}", "sum", new_temp)

def redis_exists(key):
    return r.exists(key) > 0
