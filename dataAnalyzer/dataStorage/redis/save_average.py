import redis
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)  # Added for flexibility
redis_db = os.getenv("REDIS_DB", 0)  # Added for flexibility


def get_redis_connection():
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)


r = get_redis_connection()


class SaveAverage:
    # save data of temperature for calculation in Redis
    @staticmethod
    def initialize_location_stats(city):
        r.hset(f"temp_stats:{city}", "count", 0)
        r.hset(f"temp_stats:{city}", "sum", 0.0)

    @staticmethod
    def update_location_stats(city, new_temp):
        r.hincrby(f"temp_stats:{city}", "count", 1)
        r.hincrbyfloat(f"temp_stats:{city}", "sum", new_temp)

    # save data of humidity for calculation in Redis
    @staticmethod
    def initialize_location_stats_humidity(city):
        r.hset(f"humidity_stats:{city}", "count", 0)
        r.hset(f"humidity_stats:{city}", "sum", 0.0)

    @staticmethod
    def update_location_stats_humidity(city, new_humidity):
        r.hincrby(f"humidity_stats:{city}", "count", 1)
        r.hincrbyfloat(f"humidity_stats:{city}", "sum", new_humidity)

    # redis key exist
    @staticmethod
    def redis_exists(key):
        return r.exists(key) > 0

    @staticmethod
    def redis_exists_humidity(key):
        return r.exists(key) > 0
