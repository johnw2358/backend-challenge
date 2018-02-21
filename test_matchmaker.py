#!/Applications/anaconda/bin/python

import os
import csv
import unittest
import pandas as pd
import datetime
import pytz
import calendar
from email.utils import parseaddr
from class_module import Pickup, Recipient
from matchmaker import *

class TestStringMethods(unittest.TestCase):
#    def setUp(self):
#       with open("test_pickups.csv", "w") as f:
#           writer = csv.writer(f)

#writer.writerow(["Date", "temperature 1", "Temperature 2"])
        
#        test_pickups = open("test_pickups.csv", "w")
#        test_pickups.writerow("FirstName,LastName,Street,City,State,Postal,Country,Email,Phone,Latitude,Longitude,Categories,PickupAt,TimeZoneId")
#        test_pickups.write("Brett,Sullivan,2784 Ella Street,San Francisco,CA,94107,US,BrettJSullivan@teleworm.us,650-262-4366,37.728912,-122.324225,45,2016-11-29T16:00:00-08:00,America/Los_Angeles")
#        test_pickups.close()
#self.addCleanup(os.remove, "test_pickups.csv")

    def test_load_pickups(self):
        try:
            pickups = load_pickups("Pickups.csv")
            self.pickups = pickups
        except:
            raise Exception("Error loading pickups csv file")

        for pickup in pickups:
            self.assertEquals(type(pickup.FirstName), str)
            self.assertEquals(len(pickup.FirstName.split(" ")), 1)
            
            self.assertEquals(type(pickup.LastName), str)
            self.assertEquals(len(pickup.LastName.split(" ")), 1)
            
            self.assertEquals(type(pickup.Street), str)
            try:
                int(pickup.Street.split(" ")[0])
            except:
                raise Exception("Invalid street number")
            
            self.assertEquals(type(pickup.City), str)

            self.assertEquals(type(pickup.State), str)
    
            self.assertEquals(type(pickup.Postal), int)
            self.assertEquals(len(str(pickup.Postal)), 5)
            
            self.assertEquals(type(pickup.Country), str)
            
            self.assertEquals(type(pickup.Email), str)
            self.assertNotEqual(parseaddr(pickup.Email), ("", ""))
    
            self.assertEquals(type(pickup.Phone), str)
            self.assertEquals(len(pickup.Phone.split("-")[0]), 3)
            self.assertEquals(len(pickup.Phone.split("-")[1]), 3)
            self.assertEquals(len(pickup.Phone.split("-")[2]), 4)
            try:
                int(pickup.Phone.split("-")[0])
                int(pickup.Phone.split("-")[1])
                int(pickup.Phone.split("-")[2])
            except:
                raise Exception("Invalid phone number")

            self.assertEquals(type(pickup.Latitude), float)
            self.assertTrue(-90.0 <= pickup.Latitude <= 90.0)

            self.assertEquals(type(pickup.Longitude), float)
            self.assertTrue(-180.0 <= pickup.Longitude <= 180.0)

            self.assertEquals(type(pickup.Categories), int)
            self.assertTrue(0 <= pickup.Categories < pow(2, 6))

            self.assertEquals(type(pickup.PickupAt), datetime.datetime)
            self.assertEquals(type(pickup.TimeZoneId), str)
            self.assertTrue(pickup.TimeZoneId in pytz.all_timezones)

    def test_load_recipients(self):
        try:
            recipients = load_recipients("Recipients.csv")
            self.recipients = recipients
        except:
            raise Exception("Error loading recipients csv file")

        for recipient in recipients:
            self.assertEquals(type(recipient.FirstName), str)
            self.assertEquals(len(recipient.FirstName.split(" ")), 1)

            self.assertEquals(type(recipient.LastName), str)
            self.assertEquals(len(recipient.LastName.split(" ")), 1)

            self.assertEquals(type(recipient.Street), str)
            try:
                int(recipient.Street.split(" ")[0])
            except:
                raise Exception("Invalid street number")

            self.assertEquals(type(recipient.City), str)

            self.assertEquals(type(recipient.State), str)

            self.assertEquals(type(recipient.Postal), int)
            self.assertEquals(len(str(recipient.Postal)), 5)

            self.assertEquals(type(recipient.Country), str)

            self.assertEquals(type(recipient.Email), str)
            self.assertNotEqual(parseaddr(recipient.Email), ("", ""))

            self.assertEquals(type(recipient.Phone), str)
            self.assertEquals(len(recipient.Phone.split("-")[0]), 3)
            self.assertEquals(len(recipient.Phone.split("-")[1]), 3)
            self.assertEquals(len(recipient.Phone.split("-")[2]), 4)
            try:
                int(recipient.Phone.split("-")[0])
                int(recipient.Phone.split("-")[1])
                int(recipient.Phone.split("-")[2])
            except:
                raise Exception("Invalid phone number")

            self.assertEquals(type(recipient.Latitude), float)
            self.assertTrue(-90.0 <= recipient.Latitude <= 90.0)

            self.assertEquals(type(recipient.Longitude), float)
            self.assertTrue(-180.0 <= recipient.Longitude <= 180.0)

            self.assertEquals(type(recipient.Restrictions), int)
            self.assertTrue(0 <= recipient.Restrictions < pow(2, 6))

            for weekday in list(calendar.day_name):
                self.assertEqual(type(recipient.Schedule[weekday]), int)
                self.assertTrue(0 <= recipient.Schedule[weekday] <= pow(2, 16))

#    def test_group_pickups(self):
#        try:
#            daily_pickups = group_pickups(self.pickups)
#            print("skip")
#        except:
#            raise Exception("Error grouping pickups")

#  for date, pickups in sorted(daily_pickups.items()):
#           self.assertGreater(len(pickups), 0)

    def test_calculate_distance(self):
        try:
            pickups = load_pickups("Pickups.csv")
            recipients = load_recipients("Recipients.csv")

            for pickup in pickups:
                for recipient in recipients:
                    pickup_coordinates = (pickup.Latitude, pickup.Longitude)
                    recipient_coordinates = (recipient.Latitude, recipient.Longitude)
                    distance = vincenty(pickup_coordinates, recipient_coordinates).miles
        except:
            raise Exception("Error calculating distance")

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()


