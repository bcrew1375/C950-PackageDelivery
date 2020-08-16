class Parcel:
    parcel_id = 0
    parcel_address = ""
    parcel_city = ""
    parcel_state = ""
    parcel_zip = ""
    parcel_delivery_deadline = ""
    parcel_mass_kilos = 0

    def __init__(self, record):
        self.parcel_id = record[0]
        self.parcel_address = record[1]
        self.parcel_city = record[2]
        self.parcel_state = record[3]
        self.parcel_zip = record[4]
        self.parcel_delivery_deadline = record[5]
        self.parcel_mass_kilos = record[6]

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

    def get_parcel_delivery_deadline(self):
        return self.parcel_delivery_deadline

    def set_parcel_delivery_deadline(self, parcel_delivery_deadline):
        self.parcel_delivery_deadline = parcel_delivery_deadline

    def get_parcel_mass_kilos(self):
        return int(self.parcel_mass_kilos)

    def set_parcel_mass_kilos(self, parcel_mass_kilos):
        self.parcel_mass_kilos = parcel_mass_kilos
