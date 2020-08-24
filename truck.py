class Truck:
    def __init__(self):
        self.loaded_packages = []
        self.driving_speed = 18
        self.number_loaded = 0
        self.at_hub = True
        self.depart_time = ""
        self.current_time = ""
        self.miles_driven = 0
        self.capacity = 16
        self.current_location = "HUB"

    def add_package(self, parcel_id):
        self.loaded_packages.append(parcel_id)
        self.number_loaded += 1

    def remove_package(self, parcel_id):
        self.loaded_packages.remove(parcel_id)
        self.number_loaded -= 1

    def get_loaded_packages(self):
        return self.loaded_packages

    def get_capacity(self):
        return self.capacity

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_current_location(self):
        return self.current_location

    def set_current_location(self, location):
        self.current_location = location

    def get_depart_time(self):
        return self.depart_time

    def set_depart_time(self, depart_time):
        self.depart_time = depart_time

    def get_current_time(self):
        return self.current_time

    def set_current_time(self, current_time):
        self.current_time = current_time

    def get_driving_speed(self):
        return self.driving_speed

    def set_driving_speed(self, speed):
        self.driving_speed = speed

    def get_miles_driven(self):
        return self.miles_driven

    def set_miles_driven(self, miles):
        self.miles_driven = miles

    def get_number_loaded(self):
        return self.number_loaded

    def set_number_loaded(self, number):
        self.number_loaded = number

    def get_at_hub(self):
        return self.at_hub

    def set_at_hub(self, status):
        self.at_hub = status
