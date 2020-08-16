import csv
from hashtable import HashTable
from parcel import Parcel

filename = "WGUPS Package File.csv"

parcel_records = []
parcel_table = HashTable()

with open(filename, 'r') as package_file:
    csv_parcels = csv.reader(package_file)

    # Move to line 9.
    while csv_parcels.line_num is not 11:
        next(csv_parcels)

    for parcel in csv_parcels:
        parcel_records.append(Parcel(tuple(parcel)))

    # Assign every package to a hash table entry.
    for parcel in parcel_records:
        parcel_table.insert(parcel)

    test_record = ["121", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    parcel_table.insert(Parcel(test_record))

    test_record = ["81", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    parcel_table.insert(Parcel(test_record))

    test_record = ["241", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    parcel_table.insert(Parcel(test_record))

    print(parcel_table.search(parcel_records[33]).get_parcel_address())
