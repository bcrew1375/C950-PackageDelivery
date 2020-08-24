import csv
import time

from distancetable import DistanceTable
from hashtable import HashTable
from parcel import Parcel
from truck import Truck

parcel_table = None
distance_table = None

truck_1 = Truck()
truck_2 = Truck()
truck_3 = Truck()  # Truck 3 will not be used, as there are only 2 drivers.


# Convert a time of format HH:MM AM/PM to minutes past midnight.
def convert_timestamp_to_minutes(timestamp):
    time_object = time.strptime(timestamp, "%I:%M %p")
    time_in_minutes = (int(time_object.tm_hour) * 60) + (int(time_object.tm_min))

    return time_in_minutes


def convert_minutes_to_timestamp(minutes):
    timestamp = time.strftime("%#I:%M %p", time.gmtime(minutes * 60))

    return timestamp


def get_status_list(timestamp):
    global parcel_table

    status_list = []

    for i in range (1, parcel_table.get_table_length(), 1):
        id = parcel_table.search(i).get_parcel_id()
        address = parcel_table.search(i).get_parcel_address()
        city = parcel_table.search(i).get_parcel_city()
        state = parcel_table.search(i).get_parcel_state()
        zip = parcel_table.search(i).get_parcel_zip()
        mass = parcel_table.search(i).get_parcel_mass_kilos()
        dispatch_time = convert_timestamp_to_minutes(parcel_table.search(i).get_parcel_dispatch_time())
        delivery_time = convert_timestamp_to_minutes(parcel_table.search(i).get_parcel_delivery_time())

        time_to_check = convert_timestamp_to_minutes(timestamp)

        if time_to_check < dispatch_time:
            status = "At Hub"
        elif (time_to_check >= dispatch_time) and (time_to_check < delivery_time):
            status = "En route"
        elif time_to_check >= delivery_time:
            status = "Delivered at: " + parcel_table.search(i).get_parcel_delivery_time()

        status_list.append([str(id), address, city, state, zip, str(mass), status])

    return status_list


def handle_special_notes():
    global parcel_table
    global truck_1, truck_2

    # Correct package 9's address and delay it until 10:20 AM.
    parcel_table.search(9).set_parcel_address("410 S State St")

    # Mark delayed packages.
    parcel_table.search(6).set_parcel_delayed(True)
    parcel_table.search(9).set_parcel_delayed(True)
    parcel_table.search(25).set_parcel_delayed(True)
    parcel_table.search(28).set_parcel_delayed(True)
    parcel_table.search(32).set_parcel_delayed(True)

    # Truck 1 will carry all packages that must be shipped together.
    truck_1.add_package(13)
    parcel_table.search(13).set_parcel_loaded(True)
    truck_1.add_package(14)
    parcel_table.search(14).set_parcel_loaded(True)
    truck_1.add_package(15)
    parcel_table.search(15).set_parcel_loaded(True)
    truck_1.add_package(16)
    parcel_table.search(16).set_parcel_loaded(True)
    truck_1.add_package(19)
    parcel_table.search(19).set_parcel_loaded(True)
    truck_1.add_package(20)
    parcel_table.search(20).set_parcel_loaded(True)

    # Load all packages restricted to truck 2.
    truck_2.add_package(3)
    parcel_table.search(3).set_parcel_loaded(True)
    truck_2.add_package(18)
    parcel_table.search(18).set_parcel_loaded(True)
    truck_2.add_package(36)
    parcel_table.search(36).set_parcel_loaded(True)
    truck_2.add_package(38)
    parcel_table.search(38).set_parcel_loaded(True)


def load_tables():
    global parcel_table
    global distance_table

    parcel_table = HashTable()

    distance_records = []
    parcel_records = []

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

    #test_record = ["121", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    #parcel_table.insert(Parcel(test_record))

    #test_record = ["81", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    #parcel_table.insert(Parcel(test_record))

    #test_record = ["241", "123 Fake St", "Salt Lake City", "UT", "84115", "10:30 AM", "21"]
    #parcel_table.insert(Parcel(test_record))

    filename = "WGUPS Distance Table.csv"

    with open(filename, 'r') as distance_file:
        csv_distances = csv.reader(distance_file)

        for record in csv_distances:
            distance_records.append(record)

    distance_file.close()

    distance_table = DistanceTable(distance_records)


def run_delivery_algorithm():
    global parcel_table
    global distance_table
    global truck_1, truck_2

    # Handle package special notes.
    handle_special_notes()

    # Create a list of packages that each truck will be responsible to deliver excluding special cases.
    truck_1_package_list = []
    truck_2_package_list = []

    # Determine which package will go to which truck. Truck 2 will be loaded with all delayed packages and packages
    # with a delivery deadline later than or equal to 12:00 PM. Truck 1 will be loaded with all earlier packages.
    # Trucks will carry a maximum of 16 packages.
    for i in range(1, parcel_table.get_table_length(), 1):
        current_parcel = parcel_table.search(i)
        delivery_deadline = convert_timestamp_to_minutes(current_parcel.get_parcel_delivery_deadline())

        if (delivery_deadline < convert_timestamp_to_minutes("12:00 PM")) and (current_parcel.get_parcel_loaded() is False):
            truck_1_package_list.append(current_parcel.get_parcel_id())
        elif (delivery_deadline >= convert_timestamp_to_minutes("12:00 PM")) and (current_parcel.get_parcel_loaded() is False):
            truck_2_package_list.append(current_parcel.get_parcel_id())

    truck_1.set_depart_time("8:00 AM")
    truck_1.set_current_time("8:00 AM")
    truck_2.set_depart_time("9:05 AM")
    truck_2.set_current_time("12:00 PM")

    number_of_packages = parcel_table.get_table_length()

    # Continue until all packages are delivered.
    while number_of_packages > 0:

        # Check if either truck is at the hub and load them with packages.
        if truck_1.get_at_hub() is True or truck_2.get_at_hub() is True:
            for p in range(1, parcel_table.get_table_length(), 1):
                current_parcel = parcel_table.search(p)

                if (current_parcel.get_parcel_id() in truck_1_package_list) and (truck_1.get_number_loaded() < truck_1.get_capacity())\
                        and truck_1.get_at_hub() is True:
                    truck_1.add_package(p)
                    truck_1_package_list.remove(str(p))
                elif (current_parcel.get_parcel_id() in truck_2_package_list) and (truck_2.get_number_loaded() < truck_2.get_capacity())\
                        and truck_2.get_at_hub() is True:
                    truck_2.add_package(p)
                    truck_2_package_list.remove(str(p))

        while truck_1.get_number_loaded() > 0:
            earliest_deadline = None
            delivered_parcel_id = None

            # Determine the next package to deliver prioritizing the earliest delivery deadline.
            truck_1.set_at_hub(False)

            for i in range(0, truck_1.get_number_loaded(), 1):
                parcel_id = int(parcel_table.search(truck_1.get_loaded_packages()[i]).get_parcel_id())

                if earliest_deadline is None:
                    earliest_deadline = convert_timestamp_to_minutes(parcel_table.search(parcel_id).get_parcel_delivery_deadline())
                    delivered_parcel_id = parcel_id
                else:
                    deadline = convert_timestamp_to_minutes(parcel_table.search(parcel_id).get_parcel_delivery_deadline())

                    if deadline < earliest_deadline:
                        earliest_deadline = deadline
                        delivered_parcel_id = parcel_id

            from_address = truck_1.get_current_location()
            to_address = parcel_table.search(delivered_parcel_id).get_parcel_address()
            distance = float(distance_table.get_distance(from_address, to_address))

            # Mark the parcel's delivery time and update truck 1's time.

            # Update truck 1's location and distance traveled.
            truck_1.set_miles_driven(truck_1.get_miles_driven() + distance)
            truck_1.set_current_location(to_address)

            minutes_traveled = int(distance / float(truck_1.get_driving_speed() / 60))
            current_time = convert_timestamp_to_minutes(truck_1.get_depart_time()) + minutes_traveled

            truck_1.set_current_time(convert_minutes_to_timestamp(current_time))
            truck_1.set_depart_time(convert_minutes_to_timestamp(current_time))

            loaded_packages = truck_1.get_loaded_packages().copy()

            for i in range(0, truck_1.get_number_loaded(), 1):
                parcel_id = loaded_packages[i]

                if parcel_table.search(parcel_id).get_parcel_address() == to_address:
                    truck_1.remove_package(parcel_id)
                    parcel_table.search(parcel_id).set_parcel_delivery_time(truck_1.get_current_time())

        truck_2.set_at_hub(False)

        while truck_2.get_number_loaded() > 0:
            earliest_deadline = None
            delivered_parcel_id = None

            # Determine the next package to deliver prioritizing the earliest delivery deadline.
            for i in range(0, truck_2.get_number_loaded(), 1):
                parcel_id = int(parcel_table.search(truck_2.get_loaded_packages()[i]).get_parcel_id())

                if earliest_deadline is None:
                    earliest_deadline = convert_timestamp_to_minutes(parcel_table.search(parcel_id).get_parcel_delivery_deadline())
                    delivered_parcel_id = parcel_id
                else:
                    deadline = convert_timestamp_to_minutes(parcel_table.search(parcel_id).get_parcel_delivery_deadline())

                    if deadline < earliest_deadline:
                        earliest_deadline = deadline
                        delivered_parcel_id = parcel_id


            from_address = truck_1.get_current_location()
            to_address = parcel_table.search(delivered_parcel_id).get_parcel_address()
            distance = float(distance_table.get_distance(from_address, to_address))

            # Mark the parcel's delivery time and update truck 1's time.

            # Update truck 1's location and distance traveled.
            truck_2.set_miles_driven(truck_2.get_miles_driven() + distance)
            truck_2.set_current_location(to_address)

            minutes_traveled = int(distance / float(truck_2.get_driving_speed() / 60))
            current_time = convert_timestamp_to_minutes(truck_2.get_depart_time()) + minutes_traveled

            truck_2.set_current_time(convert_minutes_to_timestamp(current_time))
            truck_2.set_depart_time(convert_minutes_to_timestamp(current_time))

            loaded_packages = truck_2.get_loaded_packages().copy()

            for i in range(0, truck_2.get_number_loaded(), 1):
                parcel_id = loaded_packages[i]

                if parcel_table.search(parcel_id).get_parcel_address() == to_address:
                    truck_2.remove_package(parcel_id)
                    parcel_table.search(parcel_id).set_parcel_delivery_time(truck_2.get_current_time())

        number_of_packages -= 1

    print("All packages delivered with truck 1 driving {0} miles and truck 2 driving {1} miles totaling {2} miles.".format(
        truck_1.get_miles_driven(), truck_2.get_miles_driven(), truck_1.get_miles_driven() + truck_2.get_miles_driven()))
    print()
