#!/Applications/anaconda/bin/python

import os
import csv
import argparse
import calendar
import pandas as pd
from dateutil import parser
from geopy.distance import vincenty

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

# Read csv filenames from user
def get_arguments():
    parser = argparse.ArgumentParser(description="Used for csv filename input")

    parser.add_argument("--pickups", type=str, required=True, help="csv filename containing pickups")
    parser.add_argument("--recipients", type=str, required=True, help="csv filename containing recipients")
    parser.add_argument("--matches", type=str, required=True, help="csv filename to write matches")
    arguments = parser.parse_args()

    return arguments

# Verify csv filename arguments
def verify_arguments(arguments):
    mandatory_arguments = {"pickups", "recipients", "matches"}

    if not mandatory_arguments.issubset(set(dir(arguments))):
        raise Exception("Missing arguements")

    if not os.path.exists(arguments.pickups):
        raise Exception("Cannot find csv filename %s specified by --pickups" % arguments.pickups)

    if not os.path.exists(arguments.recipients):
        raise Exception("Cannot find csv filename %s specified by --recipients" % arguments.recipients)

    if os.path.exists(arguments.matches):
        choice = input("Overwrite %s? [y]:" % arguments.matches) or "y"
        
        if choice.lower() != "y":
            raise Exception("The csv filename %s specified by --matches already exists" % arguments.matches)

# Load pickups from csv and convert to objects
def load_pickups(csv_filename):
    # Read csv into pandas dataframe to easily format rows
    # for Pickup class instance initialization
    df = pd.read_csv(csv_filename)
    dict_df = df.to_dict(orient="index")

    pickups = []

    for index, entry in dict_df.items():
        pickups.append(Pickup(entry))

    pickups.sort(key=lambda pickup: pickup.PickupAt)

    return pickups

# Load recipients from csv and convert to objects
def load_recipients(csv_filename):
    # Read csv into pandas dataframe to easily format rows
    # for Recipient class instance initialization
    df = pd.read_csv(csv_filename)
    dict_df = df.to_dict(orient="index")

    recipients = []

    for index, entry in dict_df.items():
        recipients.append(Recipient(entry))

    return recipients

# Group pickups by date in a dictionary
def group_pickups(pickups):
    daily_pickups = {}

    for pickup in pickups:
        date = pickup.PickupAt.strftime('%Y-%m-%d')

        if date not in daily_pickups:
            daily_pickups.update({date: [pickup]})
        else:
            daily_pickups[date].append(pickup)

    return daily_pickups

# Calculate Vincenty distance between pickup and recipient
def calculate_distance(pickup, recipient):
    pickup_coordinates = (pickup.Latitude, pickup.Longitude)
    recipient_coordinates = (recipient.Latitude, recipient.Longitude)
    
    return vincenty(pickup_coordinates, recipient_coordinates).miles

# Find all eligible recipients within 5 miles
def find_matches(pickup, recipients):
    eligible = []
    
    for recipient in recipients:
        if pickup.Categories & recipient.Restrictions == 0:
            distance = calculate_distance(pickup, recipient)    
    
            # Magic number 5 is the maximum distance in miles for a recipient
            if distance < 5 and recipient.is_open(pickup.PickupAt):
                    eligible.append((recipient, distance))

    return sorted(eligible, key=lambda recipient_tuple: recipient_tuple[1])

# Write eligible matches for each pickup to a csv
def write_results(filename, daily_pickups):
    with open(filename, "w") as csvfile:
        writer=csv.writer(csvfile, delimiter=",")

        for date, pickups in sorted(daily_pickups.items()):
           for pickup in pickups:
                row = [date, pickup.full_name()] 

                if len(pickup.Matches) > 0:
                    for match, distance in pickup.Matches:
                        row.append(match.full_name())
                        row.append(str(round(distance, 2)))
                else:
                    row.append("None")
            
                writer.writerow(row)

# Match recipients to each pickup
def assign_matches(daily_pickups, recipients):
    for date, pickups in sorted(daily_pickups.items()):
        for pickup in pickups:
            matches = find_matches(pickup, recipients)

            if len(matches) > 0:
                pickup.Matches = matches
def main():
    # Read and verify arguments
    arguments = get_arguments()
    verify_arguments(arguments)

    # Load csv files and convert pickups and recipients to objects
    pickups = load_pickups(arguments.pickups)
    recipients = load_recipients(arguments.recipients)

    # Group pickups by date in a dictionary
    daily_pickups = group_pickups(pickups)

    # Match recipients to each pickup
    assign_matches(daily_pickups, recipients) 

    # Write eligible matches for each pickup to a csv
    write_results(arguments.matches, daily_pickups)

if __name__ == "__main__":
    main()

