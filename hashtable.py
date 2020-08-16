# creates a table to store package objects. Hash table has a max index of 39
# with higher package ids being stored in a list.
class HashTable:
    table_array = [None] * 40

    def __init__(self):
        for i in range(0, len(self.table_array), 1):
            self.table_array[i] = [None]

    def computehash(self, parcel):
        return (int(parcel.get_parcel_id()) - 1) % 40

    def insert(self, parcel):
        # Calculate the parcel's bucket index.
        table_bucket_index = self.computehash(parcel)

        # Calculate the parcel's index in the list for the bucket.
        table_list_index = int((int(parcel.get_parcel_id()) - 1) / 40)

        # Extend the bucket's list size if needed to accommodate the new entry.
        if len(self.table_array[table_bucket_index]) < table_list_index:
            append_list = [None] * (table_list_index - len(self.table_array[table_bucket_index]))
            append_list.append(parcel)
            self.table_array[table_bucket_index].extend(append_list)
        else:
            self.table_array[table_bucket_index][table_list_index] = parcel

        #self.table_array.insert(self.computehash(parcel), parcel)

    def search(self, parcel):
        return self.table_array[self.computehash(parcel)]
