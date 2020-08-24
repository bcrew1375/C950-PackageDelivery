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

    for i in range(1, parcel_table.get_table_length() + 1, 1):
        id = parcel_table.search(i).get_parcel_id()
        address = parcel_table.search(i).get_parcel_address()
        city = parcel_table.search(i).get_parcel_city()
        state = parcel_table.search(i).get_parcel_state()
        zip = parcel_table.search(i).get_parcel_zip()
        mass = parcel_table.search(i).get_parcel_mass_kilos()
        depart_time = convert_timestamp_to_minutes(parcel_table.search(i).get_parcel_depart_time())
        delivery_time = convert_timestamp_to_minutes(parcel_table.search(i).get_parcel_delivery_time())

        time_to_check = convert_timestamp_to_minutes(timestamp)

        if time_to_check < depart_time:
            status = "At Hub"
        elif (time_to_check >= depart_time) and (time_to_check < delivery_time):
            status = "En route"
        elif time_to_check >= delivery_time:
            status = "Delivered at: " + parcel_table.search(i).get_parcel_delivery_time()

        status_list.append([str(id), address, city, state, zip, str(mass), status])

    return status_list


#def handle_special_notes():
#    global parcel_table
#    global truck_1, truck_2


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

    # Create a list of packages that each truck will be responsible to deliver.
    truck_1_package_list = []
    truck_2_package_list = []

    # Determine which package will go to which truck.
    truck_to_load = 1

    for i in range(1, parcel_table.get_table_length() + 1, 1):
        current_parcel = parcel_table.search(i)
        delivery_deadline = convert_timestamp_to_minutes(current_parcel.get_parcel_delivery_deadline())

        # Evenly distribute packages with an early deadline to each truck.
        if (delivery_deadline < convert_timestamp_to_minutes("12:00 PM")) and (current_parcel.get_parcel_assigned() is False):
            if truck_to_load == 1:
                truck_1_package_list.append(current_parcel.get_parcel_id())
                current_parcel.set_parcel_assigned(True)
                truck_to_load = 2
            elif truck_to_load == 2:
                truck_2_package_list.append(current_parcel.get_parcel_id())
                current_parcel.set_parcel_assigned(True)
                truck_to_load = 1

    # Handle package special notes.
    #handle_special_notes()

    # Correct package 9's address and delay it until 10:20 AM.
    parcel_table.search(9).set_parcel_address("410 S State St")

    # Truck 1 will carry all packages that must be shipped together.
    #truck_1_package_list.append(13)
    #parcel_table.search(13).set_parcel_assigned(True)
    truck_2_package_list.remove(14)
    truck_1_package_list.append(14)
    parcel_table.search(14).set_parcel_assigned(True)
    #truck_1_package_list.append(15)
    #parcel_table.search(15).set_parcel_assigned(True)
    truck_2_package_list.remove(16)
    truck_1_package_list.append(16)
    parcel_table.search(16).set_parcel_assigned(True)
    truck_1_package_list.append(19)
    parcel_table.search(19).set_parcel_assigned(True)
    #truck_1_package_list.append(20)
    #parcel_table.search(20).set_parcel_assigned(True)

    # Load all packages restricted and delayed to truck 2.
    truck_2_package_list.append(3)
    parcel_table.search(3).set_parcel_assigned(True)
    truck_2_package_list.append(18)
    parcel_table.search(18).set_parcel_assigned(True)
    truck_2_package_list.append(36)
    parcel_table.search(36).set_parcel_assigned(True)
    truck_2_package_list.append(38)
    parcel_table.search(38).set_parcel_assigned(True)

    #truck_2_package_list.append(6)
    #parcel_table.search(6).set_parcel_assigned(True)
    truck_2_package_list.append(9)
    parcel_table.search(9).set_parcel_assigned(True)
    #truck_2_package_list.append(25)
    #parcel_table.search(25).set_parcel_assigned(True)
    truck_2_package_list.append(28)
    parcel_table.search(28).set_parcel_assigned(True)
    truck_2_package_list.append(32)
    parcel_table.search(32).set_parcel_assigned(True)

    # Distribute remaining packages.
    truck_to_load = 1

    for i in range(1, parcel_table.get_table_length() + 1, 1):
        current_parcel = parcel_table.search(i)

        # If more than one package is going to an address, assign them to the same truck.
        if current_parcel.get_parcel_assigned() is False:
            for j in range(0, len(truck_1_package_list), 1):
                current_address = current_parcel.get_parcel_address()
                list_address = parcel_table.search(truck_1_package_list[j]).get_parcel_address()

                if current_address == list_address:
                    truck_1_package_list.append(current_parcel.get_parcel_id())
                    current_parcel.set_parcel_assigned(True)


        if current_parcel.get_parcel_assigned() is False:
            for j in range(0, len(truck_2_package_list), 1):
                current_address = current_parcel.get_parcel_address()
                list_address = parcel_table.search(truck_2_package_list[j]).get_parcel_address()

                if current_address == list_address:
                    truck_2_package_list.append(current_parcel.get_parcel_id())
                    current_parcel.set_parcel_assigned(True)


        # If the package is still unassigned, alternate truck assignments.
        if current_parcel.get_parcel_assigned() is False:
            if truck_to_load == 1:
                truck_1_package_list.append(current_parcel.get_parcel_id())
                truck_to_load = 2
            elif truck_to_load == 2:
                truck_2_package_list.append(current_parcel.get_parcel_id())
                truck_to_load = 1


    truck_1.set_depart_time("8:00 AM")
    truck_1.set_current_time("8:00 AM")
    truck_2.set_depart_time("9:05 AM")
    truck_2.set_current_time("9:05 AM")

    number_of_packages_left = parcel_table.get_table_length()

    # Continue until all packages are delivered.
    while number_of_packages_left > 0:

        # Check if either truck is at the hub and load them with packages.
        # Trucks will carry a maximum of 16 packages.
        if truck_1.get_at_hub() is True or truck_2.get_at_hub() is True:
            truck_1_current_list = truck_1_package_list.copy()

            for i in range(0, len(truck_1_package_list), 1):
                current_parcel = parcel_table.search(truck_1_current_list[i])

                if (current_parcel.get_parcel_id() in truck_1_package_list) and (truck_1.get_number_loaded() < truck_1.get_capacity())\
                        and truck_1.get_at_hub() is True:
                    truck_1.add_package(current_parcel.get_parcel_id())
                    truck_1_package_list.remove(current_parcel.get_parcel_id())

            truck_2_current_list = truck_2_package_list.copy()

            for i in range(0, len(truck_2_package_list), 1):
                current_parcel = parcel_table.search(truck_2_current_list[i])

                if (current_parcel.get_parcel_id() in truck_2_package_list) and (truck_2.get_number_loaded() < truck_2.get_capacity())\
                        and truck_2.get_at_hub() is True:
                    truck_2.add_package(current_parcel.get_parcel_id())
                    truck_2_package_list.remove(current_parcel.get_parcel_id())

        # Truck 1 has departed the hub.
        truck_1.set_at_hub(False)

        for i in range(0, truck_1.get_number_loaded(), 1):
            parcel_table.search(truck_1.get_loaded_packages()[i]).set_parcel_depart_time(truck_1.get_current_time())

        while truck_1.get_number_loaded() > 0:
            earliest_deadline = None
            delivered_parcel_id = None

            # Determine the next package to deliver prioritizing the earliest delivery deadline.
            from_address = truck_1.get_current_location()

            for i in range(0, truck_1.get_number_loaded(), 1):
                parcel_id = int(parcel_table.search(truck_1.get_loaded_packages()[i]).get_parcel_id())

                if earliest_deadline is None:
                    earliest_deadline = convert_timestamp_to_minutes(parcel_table.search(parcel_id).get_parcel_delivery_deadline())
                    to_address = parcel_table.search(parcel_id).get_parcel_address()
                else:
                    deadline = convert_timestamp_to_minutes(parcel_table.search(parcel_id).get_parcel_delivery_deadline())

                    if deadline < earliest_deadline:
                        earliest_deadline = deadline
                        to_address = parcel_table.search(parcel_id).get_parcel_address()
                    # If two deadlines are the same, determine which has the shortest distance.
                    elif deadline == earliest_deadline:
                        distance_1 = distance_table.get_distance(from_address, to_address)
                        distance_2 = distance_table.get_distance(from_address, parcel_table.search(parcel_id).get_parcel_address())

                        if distance_2 < distance_1:
                            to_address = parcel_table.search(parcel_id).get_parcel_address()

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

            # Remove any additional packages for the same address.
            for i in range(0, truck_1.get_number_loaded(), 1):
                parcel_id = loaded_packages[i]

                if parcel_table.search(parcel_id).get_parcel_address() == to_address:
                    truck_1.remove_package(parcel_id)
                    number_of_packages_left -= 1
                    parcel_table.search(parcel_id).set_parcel_delivery_time(truck_1.get_current_time())


        truck_2.set_at_hub(False)

        for i in range(0, truck_2.get_number_loaded(), 1):
            parcel_table.search(truck_2.get_loaded_packages()[i]).set_parcel_depart_time(truck_2.get_current_time())

        while truck_2.get_number_loaded() > 0:
            earliest_deadline = None

            # Determine the next package to deliver prioritizing the earliest delivery deadline.
            from_address = truck_2.get_current_location()

            for i in range(0, truck_2.get_number_loaded(), 1):
                parcel_id = int(parcel_table.search(truck_2.get_loaded_packages()[i]).get_parcel_id())

                if earliest_deadline is None:
                    earliest_deadline = convert_timestamp_to_minutes(parcel_table.search(parcel_id).get_parcel_delivery_deadline())
                    to_address = parcel_table.search(parcel_id).get_parcel_address()
                else:
                    deadline = convert_timestamp_to_minutes(
                        parcel_table.search(parcel_id).get_parcel_delivery_deadline())

                    if deadline < earliest_deadline:
                        earliest_deadline = deadline
                        to_address = parcel_table.search(parcel_id).get_parcel_address()
                    # If two deadlines are the same, determine which has the shortest distance.
                    elif deadline == earliest_deadline:
                        distance_1 = distance_table.get_distance(from_address, to_address)
                        distance_2 = distance_table.get_distance(from_address, parcel_table.search(parcel_id).get_parcel_address())

                        if distance_2 < distance_1:
                            to_address = parcel_table.search(parcel_id).get_parcel_address()

            distance = float(distance_table.get_distance(from_address, to_address))

            # Mark the parcel's delivery time and update truck 2's time.

            # Update truck 2's location and distance traveled.
            truck_2.set_miles_driven(truck_2.get_miles_driven() + distance)
            truck_2.set_current_location(to_address)

            minutes_traveled = int(distance / float(truck_2.get_driving_speed() / 60))
            current_time = convert_timestamp_to_minutes(truck_2.get_depart_time()) + minutes_traveled

            truck_2.set_current_time(convert_minutes_to_timestamp(current_time))
            truck_2.set_depart_time(convert_minutes_to_timestamp(current_time))

            loaded_packages = truck_2.get_loaded_packages().copy()

            # Remove any additional packages for the same address.
            for i in range(0, truck_2.get_number_loaded(), 1):
                parcel_id = loaded_packages[i]

                if parcel_table.search(parcel_id).get_parcel_address() == to_address:
                    truck_2.remove_package(parcel_id)
                    number_of_packages_left -= 1
                    parcel_table.search(parcel_id).set_parcel_delivery_time(truck_2.get_current_time())

        if number_of_packages_left > 0:
            # Determine which truck is the shortest distance from the hub and send it back.
            truck_1_distance_to_hub = distance_table.get_distance(truck_1.get_current_location(), "HUB")
            truck_2_distance_to_hub = distance_table.get_distance(truck_2.get_current_location(), "HUB")

            if truck_1_distance_to_hub < truck_2_distance_to_hub:
                truck_1_package_list.extend(truck_2_package_list)
                truck_2_package_list.clear()
                truck_1.set_miles_driven(float(truck_1.get_miles_driven()) + float(truck_1_distance_to_hub))
                truck_1.set_at_hub(True)
            else:
                truck_2_package_list.extend(truck_1_package_list)
                truck_1_package_list.clear()
                truck_2.set_miles_driven(float(truck_2.get_miles_driven()) + float(truck_2_distance_to_hub))
                truck_2.set_at_hub(True)

    print("All packages delivered with truck 1 driving {0} miles and truck 2 driving {1} miles totaling {2} miles.".format(
        truck_1.get_miles_driven(), truck_2.get_miles_driven(), truck_1.get_miles_driven() + truck_2.get_miles_driven()))
    print()
