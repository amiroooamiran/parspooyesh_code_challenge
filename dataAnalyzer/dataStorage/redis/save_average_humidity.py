import redis
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)


def initialize_location_stats_humidity(city):
    r.hset(f"humidity_stats:{city}", "count", 0)
    r.hset(f"humidity_stats:{city}", "sum", 0.0)


def update_location_stats_humidity(city, new_humidity):
    r.hincrby(f"humidity_stats:{city}", "count", 1)
    r.hincrbyfloat(f"humidity_stats:{city}", "sum", new_humidity)


def redis_exists_humidity(key):
    return r.exists(key) > 0
