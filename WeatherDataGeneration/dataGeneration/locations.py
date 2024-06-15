import random
import time

class Location:
    @staticmethod
    def locations():
        # list of the locations
        places = ["city park", "downtown", "suburb", "Riverside", "airport"]
        citys = ["Tehran", "Abadan", "Tabriz", "Mashhad", "Isfahan", "Shiraz"]
        # Generate random location data
        finaly_location = []

        for city in citys:
            rand_place = random.choice(places)
            rand_location = f'{city} {rand_place}'
            finaly_location.append(rand_location)    
        return finaly_location