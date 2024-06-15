import random
import time

class Location:
    @staticmethod
    def locations():
        # list of the locations
        places = ["city park", "downtown", "suburb", "Riverside", "airport"]
        citys = ["Tehran", "Abadan", "Tabriz", "Mashhad", "Isfahan", "Shiraz"]
        # Generate random location data
        rand_city = random.choice(citys)
        rand_place = random.choice(places)

        return rand_city, rand_place