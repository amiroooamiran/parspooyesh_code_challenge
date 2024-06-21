class LocationSplitter:
    @staticmethod
    def split_location(location):
        parts = location.split()
        if len(parts) > 1:
            city = parts[0]
            zone = " ".join(parts[1:])
        else:
            city = parts[0]
            zone = ""
        return city, zone
