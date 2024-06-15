import random

class WindSpeed:
    def windspeed():
        rand_float = random.uniform(1.1, 46.5)
        rand_wind_speed = round(rand_float, 1)
        return rand_wind_speed