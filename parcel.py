class Parcel:
    def __init__(self, record):
        self.parcel_id = record[0]
        self.parcel_address = record[1]
        self.parcel_city = record[2]
        self.parcel_state = record[3]
        self.parcel_zip = record[4]

        # Set end of day as 5:00 PM.
        if record[5] == "EOD":
            self.parcel_delivery_deadline = "5:00 PM"
        else:
            self.parcel_delivery_deadline = record[5]

        self.parcel_mass_kilos = record[6]

        self.parcel_dispatch_time = "12:00 AM"
        self.parcel_delivery_time = "12:00 AM"
        self.parcel_loaded = False
        self.parcel_delayed = False

    def get_parcel_id(self):
        return self.parcel_id

    def set_parcel_id(self, parcel_id):
        self.parcel_id = parcel_id

    def get_parcel_address(self):
        return self.parcel_address

    def set_parcel_address(self, parcel_address):
        self.parcel_address = parcel_address

    def get_parcel_city(self):
        return self.parcel_city

    def set_parcel_city(self, parcel_city):
        self.parcel_city = parcel_city

    def get_parcel_state(self):
        return self.parcel_state

    def set_parcel_state(self, parcel_state):
        self.parcel_state = parcel_state

    def get_parcel_zip(self):
        return self.parcel_zip

    def set_parcel_zip(self, parcel_zip):
        self.parcel_zip = parcel_zip

    def get_parcel_delivery_time(self):
        return self.parcel_delivery_time

    def set_parcel_delivery_time(self, delivery_time):
        self.parcel_delivery_time = delivery_time

    def get_parcel_dispatch_time(self):
        return self.parcel_dispatch_time

    def set_parcel_dispatch_time(self, dispatch_time):
        self.parcel_dispatch_time = dispatch_time

    def get_parcel_delivery_deadline(self):
        return self.parcel_delivery_deadline

    def set_parcel_delivery_deadline(self, parcel_delivery_deadline):
        self.parcel_delivery_deadline = parcel_delivery_deadline

    def get_parcel_mass_kilos(self):
        return int(self.parcel_mass_kilos)

    def set_parcel_mass_kilos(self, parcel_mass_kilos):
        self.parcel_mass_kilos = parcel_mass_kilos

    def get_parcel_loaded(self):
        return self.parcel_loaded

    def set_parcel_loaded(self, state):
        self.parcel_loaded = state

    def get_parcel_delayed(self):
        return self.parcel_delayed

    def set_parcel_delayed(self, state):
        self.parcel_delayed = state
