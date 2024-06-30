# calculate.py

import redis
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)  # Added for flexibility
redis_db = os.getenv("REDIS_DB", 0)  # Added for flexibility


def get_redis_connection():
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)


r = get_redis_connection()


class Averages:
    @staticmethod
    def cal_average_temp_for_location(city):
        count = r.hget(f"temp_stats:{city}", "count")
        sum_of_temps = r.hget(f"temp_stats:{city}", "sum")

        if count is None or sum_of_temps is None:
            return 0

        count = int(count)
        sum_of_temps = float(sum_of_temps)

        average_temp = sum_of_temps / count if count > 0 else 0
        round_average_temp = round(average_temp, 2)
        return round_average_temp

    @staticmethod
    def cal_average_humidity_for_location(city):
        count = r.hget(f"humidity_stats:{city}", "count")
        sum_of_humidity = r.hget(f"humidity_stats:{city}", "sum")

        if count is None or sum_of_humidity is None:
            return 0

        count = int(count)
        sum_of_humidity = float(sum_of_humidity)

        average_temp = sum_of_humidity / count if count > 0 else 0
        round_average_temp = round(average_temp, 2)
        return round_average_temp
