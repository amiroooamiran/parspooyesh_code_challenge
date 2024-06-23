import redis
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

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
