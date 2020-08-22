import csv
from distancetable import DistanceTable
from hashtable import HashTable
from parcel import Parcel

distance_records = []
parcel_records = []
parcel_table = HashTable()


def load_tables():
    filename = "WGUPS Package File.csv"

    # Parse the package CSV file and store the information into a hash table.
    with open(filename, 'r') as package_file:
        csv_parcels = csv.reader(package_file)

        # Move to record 11.
        while csv_parcels.line_num is not 11:
            next(csv_parcels)

        for parcel in csv_parcels:
            parcel_records.append(Parcel(tuple(parcel)))

        # Assign every package to a hash table entry.
        for parcel in parcel_records:
            parcel_table.insert(parcel)

    package_file.close()

    test_record = ["121", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    parcel_table.insert(Parcel(test_record))

    test_record = ["81", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    parcel_table.insert(Parcel(test_record))

    test_record = ["241", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    parcel_table.insert(Parcel(test_record))

    filename = "WGUPS Distance Table.csv"

    with open(filename, 'r') as distance_file:
        csv_distances = csv.reader(distance_file)

        for record in csv_distances:
            distance_records.append(record)

    distance_file.close()

load_tables()
distance_table = DistanceTable(distance_records)

print(distance_table.get_distance("1330 2100 S", "2600 Taylorsville Blvd"))
