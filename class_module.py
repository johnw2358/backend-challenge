
import calendar
from dateutil import parser

class Pickup:
    def __init__(self, d):
        self.Matches = []

        for key, value in d.items():
            setattr(self, key, value)

        # Change PickupAt from type str to type datetime object
        self.PickupAt = parser.parse(self.PickupAt)

    def full_name(self):
        return self.FirstName + " " + self.LastName

class Recipient:
    def __init__(self, d):
        # Keep track of hours of operation in dictionary
        # e.g. {"Sunday": 44536, "Monday": 44382, ...}
        self.Schedule = {}
        weekdays = list(calendar.day_name)

        for key, value in d.items():
            if key not in weekdays:
                setattr(self, key, value)
            else:
                self.Schedule.update({key: value})

    def full_name(self):
        return self.FirstName + " " + self.LastName

    def is_open(self, datetime):
        day = datetime.strftime("%A")
        time = int(datetime.strftime("%H"))

        # Check if recipient is open for the hour after pickup
        # Magic number 8 is the hours offset for the bitpacking scheme
        if self.Schedule[day] & pow(2, time - 8) == 0:
            return True
        else:
            return False

