#!/Applications/anaconda/bin/python

import os
import csv
import unittest
#import pandas as pd
import datetime
import pytz
import calendar
from email.utils import parseaddr
from class_module import Pickup, Recipient
from matchmaker import *

class TestMethods(unittest.TestCase):
    AlreadySetup = False
    Arguments = []

    def setUp(self):
        # Read and verify csv filename arguments one time only
        if not self.__class__.AlreadySetup:
            self.__class__.AlreadySetup = True
            self.__class__.Arguments = get_arguments()
            verify_arguments(self.Arguments)

        # Create pickup data structures from input csv files to test
        try: 
            self.test_pickups = load_pickups(self.Arguments.pickups)
            self.test_recipients = load_recipients(self.Arguments.recipients)
            self.test_daily_pickups = group_pickups(self.test_pickups)
            assign_matches(self.test_daily_pickups, self.test_recipients)

        except:
            raise Exception("Error loading test data")

    # Assert proper data formatting for each pickup
    def test_load_pickups(self):
        for pickup in self.test_pickups:
            # First name is a string with no spaces
            self.assertEquals(type(pickup.FirstName), str)
            self.assertEquals(len(pickup.FirstName.split(" ")), 1)
            
            # Last name is a string with no spaces
            self.assertEquals(type(pickup.LastName), str)
            self.assertEquals(len(pickup.LastName.split(" ")), 1)
            
            # Street name is an address number followed by a string
            self.assertEquals(type(pickup.Street), str)
            try:
                int(pickup.Street.split(" ")[0])
            except:
                raise Exception("Invalid street number")
           
            # City, State and Country are all strings
            self.assertEquals(type(pickup.City), str)
            self.assertEquals(type(pickup.State), str)
            self.assertEquals(type(pickup.Country), str)

            # Postal code is a 5 digit integer
            self.assertEquals(type(pickup.Postal), int)
            self.assertEquals(len(str(pickup.Postal)), 5)
            
            # Email is properly formatted
            self.assertEquals(type(pickup.Email), str)
            self.assertNotEqual(parseaddr(pickup.Email), ("", ""))
    
            # Phone number is properly formatted
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

            # Latitude is in range (-90, 90) and a float
            self.assertEquals(type(pickup.Latitude), float)
            self.assertTrue(-90.0 <= pickup.Latitude <= 90.0)

            # Longitude is in range (-180, 180) and a float
            self.assertEquals(type(pickup.Longitude), float)
            self.assertTrue(-180.0 <= pickup.Longitude <= 180.0)

            # Categories is a properly bit packed int
            self.assertEquals(type(pickup.Categories), int)
            self.assertTrue(0 <= pickup.Categories < pow(2, 6))

            # Datetime time and timezone are valid
            self.assertEquals(type(pickup.PickupAt), datetime.datetime)
            self.assertEquals(type(pickup.TimeZoneId), str)
            self.assertTrue(pickup.TimeZoneId in pytz.all_timezones)

    # Assert proper data formatting for each recipient using similar checks as above
    def test_load_recipients(self):
        for recipient in self.test_recipients:
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

    # Assert each date and pickup is the proper type
    def test_group_pickups(self):
        for date, pickups in sorted(self.test_daily_pickups.items()):
            self.assertEqual(type(date), str)
            
            for pickup in pickups:
                self.assertEqual(type(pickup), Pickup)

    # Assert only positive distances are calculated between pickups and recipients
    def test_calculate_distance(self):
        for pickup in self.test_pickups:
            for recipient in self.test_recipients:
                distance = calculate_distance(pickup, recipient)
                self.assertGreater(distance, 0)

    # Assert matches are within 5 miles, have no overlapping restrictions and are open
    def test_find_matches(self):
        for pickup in self.test_pickups:
            matches = find_matches(pickup, self.test_recipients)
            
            for match, distance in matches:
                self.assertEqual(type(match), Recipient)
                self.assertLess(distance, 5.0)
                self.assertEqual(pickup.Categories & match.Restrictions, 0)
                self.assertTrue(match.is_open(pickup.PickupAt))

    # Assert the output matches files is written
    def test_write_results(self):
        write_results(self.Arguments.matches, self.test_daily_pickups)
        self.assertTrue(os.path.isfile("./" + self.Arguments.matches))
        # Optioanlly, remove the test matches output file asfter testing
        # os.remove("./" + self.arguments.matches)
        
    # Assert match compatibility again
    def test_assign_matches(self):
        assign_matches(self.test_daily_pickups, self.test_recipients)
        
        for pickup in self.test_pickups:
            for match, distance in pickup.Matches:
                self.assertEquals(type(match), Recipient)
                self.assertLess(distance, 5.0)
                self.assertEqual(pickup.Categories & match.Restrictions, 0)
                self.assertTrue(match.is_open(pickup.PickupAt))

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()


