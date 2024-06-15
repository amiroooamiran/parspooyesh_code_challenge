import random
import time

def locations():
    # list of the location
    places = ["city park", "downtown", "suburb", "Riverside", "airport"]
    citys = ["Tehran", "Abadan", "Tabriz", "Mashhad", "Isfahan", "Shiraz"]
    # data location generator
    while True:
        rand_city = random.choice(citys)
        rand_place = random.choice(places)
        print(rand_city, rand_place)
        time.sleep(1)

locations()
        

