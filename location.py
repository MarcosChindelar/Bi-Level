"""
@author: Chindelar
"""
# Class with the information about locations


class Location:

    def __init__(self, Id, Type, x, y, demand):

        self.id = Id
        self.type = Type
        self.x = x
        self.y = y
        self.demand = demand

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_demand(self):
        return self.demand

    def print_location_information(self):  # print all atributes of location
        print("{:^6}".format(self.get_id()),
              "\t", "{:^6}".format(self.get_type()),
              "\t", "{:^6}".format(self.get_x()),
              "\t", "{:^6}".format(self.get_y()),
              "\t", "{:^6}".format(self.get_demand()))
