from datetime import datetime


class TimeFilter:
    def __init__(self, start_time, end_time):
        self.start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        self.end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    def extract_time_components(self, time_string):
        datetime_format = "%Y-%m-%d %H:%M:%S"
        try:
            parsed_time = datetime.strptime(time_string, datetime_format)
            year = parsed_time.year
            month = parsed_time.month
            day = parsed_time.day
            hour = parsed_time.hour
            minute = parsed_time.minute
            second = parsed_time.second
            return year, month, day, hour, minute, second
        except ValueError:
            return None, None, None, None, None, None

    def is_time_in_range(self, time_string):
        try:
            current_datetime = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
            return (
                self.start_datetime <= current_datetime <= self.end_datetime
                and current_datetime.second == 0
            )
        except ValueError:
            return False
