import redis
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

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
