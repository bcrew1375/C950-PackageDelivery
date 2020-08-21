class DistanceTable:

    def __init__(self, distance_records):
        self.address_dictionary = {}

        # Go through the address column in the records and create a dictionary with each address and an adjacency list.
        for i in range(1, len(distance_records), 1):

            # Add each address to a dictionary and nest a dictionary to hold the distance of other addresses.
            self.address_dictionary[distance_records[0][i]] = {}

            # Transpose the distance table values
            for j in range(1, len(distance_records), 1):
                distance_records[i][j] = distance_records[j][i]

                # Add each address's distance to the nested dictionary of the address of column i.
                self.address_dictionary[distance_records[0][i]][distance_records[j][0]] = distance_records[j][i]

    def get_distance(self, from_address, to_address):
        return self.address_dictionary[from_address][to_address]
