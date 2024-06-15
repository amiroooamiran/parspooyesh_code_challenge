import random
import datetime

class Temperature:
    @staticmethod
    def temp(base_temp):
        # Get the current hour
        current_hour = datetime.datetime.now().hour
        
        if current_hour < 6:
            time_factor = 0
        elif current_hour < 12:
            time_factor = (current_hour - 6) / 6
        elif current_hour < 18:
            time_factor = (18 - current_hour) / 6 
        else:
            time_factor = 0
        
        # Calculate temperature based on time factor
        adjusted_temp = base_temp + (5 * time_factor) - (5 * (1 - time_factor))
        return random.uniform(adjusted_temp - 2, adjusted_temp + 2)
