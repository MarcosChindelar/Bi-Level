"""
@author: Chindelar
"""
import parameters
import sys
from location import Location


class Instance():

    def read_input_txt(self, file_name):
        parameters.ARCHIVE_NAME = file_name
        with open(file_name) as arq:
            lines = arq.readlines()
        line = lines[0].split()
        n = int(line[0])
        parameters.NUM_LOCATIONS = n
        parameters.ENERGY_CAPACITY = float(line[1])
        parameters.LOAD_CAPACITY = float(line[2])
        parameters.ENERGY_CONSUPTION = float(line[3])
        for i in range(1, n+1):
            line = lines[i].split()
            Id = line[0]
            kind = line[1]
            x = float(line[2])
            y = float(line[3])
            demand = float(line[4])
            location = Location(Id, kind, x, y, demand)
            if kind.endswith("d"):
                location = Location("D0", "d", x, y, demand)
                parameters.LOCATIONS.append(location)
            if kind.endswith("f"):
                parameters.LOCATIONS.append(location)
                parameters.STATIONS.append(i-1)
                parameters.NUM_STATIONS += 1
            if kind.endswith("c"):
                parameters.LOCATIONS.append(location)
                parameters.CUSTOMERS.append(i-1)
                parameters.NUM_CUSTOMERS += 1
        self.make_distance_matrix()

    def get_distance(self, location_a, location_b):
        distance = 0
        x_a = parameters.LOCATIONS[location_a].get_x()
        x_b = parameters.LOCATIONS[location_b].get_x()
        y_a = parameters.LOCATIONS[location_a].get_y()
        y_b = parameters.LOCATIONS[location_b].get_y()
        x = x_a - x_b
        y = y_a - y_b
        distance = (x**2 + y**2)**(1/2)

        return round(distance, 2)

    def make_distance_matrix(self):
        distance = 0
        parameters.DISTANCE_MATRIX = []
        parameters.DISTANCE_MATRIX = \
            [[0 for i in range(parameters.NUM_LOCATIONS)]
             for j in range(parameters.NUM_LOCATIONS)]
        for i in range(parameters.NUM_LOCATIONS):
            for j in range(parameters.NUM_LOCATIONS):
                distance = self.get_distance(i, j)
                if distance != 0:
                    parameters.DISTANCE_MATRIX[i][j] = distance
                else:
                    parameters.DISTANCE_MATRIX[i][j] = 0

    def read_elem(self, filename):
        with open(filename) as f:
            return [str(elem) for elem in f.read().split()]

    def read_input_evrp(self, file_name):
        parameters.ARCHIVE_NAME = file_name[:-4]
        auxiliary = 0  # Variable for temporary conversion of values
        position = 0  # Variable for set the postions in locations list
        file_iterator = iter(self.read_elem(file_name))
        while(1):
            token = next(file_iterator)
            if token == "DIMENSION:":
                auxiliary = int(next(file_iterator))
                parameters.NUN_CUSTOMERS = auxiliary - 1
            elif token == "STATIONS:":
                auxiliary = int(next(file_iterator))
                parameters.NUN_STATIONS = auxiliary
            elif token == "CAPACITY:":
                auxiliary = float(next(file_iterator))
                parameters.load_capacity = auxiliary
            elif token == "ENERGY_CAPACITY:":
                auxiliary = float(next(file_iterator))
                parameters.energy_capacity = auxiliary
            elif token == "ENERGY_CONSUMPTION:":
                auxiliary = float(next(file_iterator))
                parameters.ENERGY_CONSUPTION = auxiliary
            elif token == "EDGE_WEIGHT_FORMAT:":
                token = next(file_iterator)
                if token != "EUC_2D":
                    print("Edge Weight Type "
                          + token + " is not supported (only EUD_2D)")
                    sys.exit(1)
            elif token == "NODE_COORD_SECTION":
                break
        parameters.NUM_LOCATIONS = parameters.NUN_CUSTOMERS\
            + parameters.NUN_STATIONS + 1
        locations_id = []
        locations_x = []
        locations_y = []
        location_id = 0
        location_x = 0
        location_y = 0
        for l in range(parameters.NUM_LOCATIONS):
            location_id = next(file_iterator)
            location_x = float(next(file_iterator))
            location_y = float(next(file_iterator))
            locations_id.append(location_id)
            locations_x.append(location_x)
            locations_y.append(location_y)
        token = next(file_iterator)
        if token != "DEMAND_SECTION":
            print("Expected token DEMAND_SECTION")
            sys.exit(1)
        locations_demand = []
        for n in range(parameters.NUN_CUSTOMERS+1):
            node_id = next(file_iterator)
            if node_id not in locations_id:
                print("Unexpected index")
                sys.exit(1)
            else:
                locations_demand.append(float(next(file_iterator)))
        token = next(file_iterator)
        if token != "STATIONS_COORD_SECTION":
            print("Expected token DEPOT_SECTION")
            sys.exit(1)
        else:
            stations = []
            for s in range(parameters.NUN_STATIONS):
                stations.append(next(file_iterator))
        token = next(file_iterator)
        if token != "DEPOT_SECTION":
            print("Expected token DEPOT_SECTION")
            sys.exit(1)
        else:
            depot_id = next(file_iterator)
            end_of_depot_section = int(next(file_iterator))
        if end_of_depot_section != -1:
            print("Expecting only one warehouse, more than one found")
            sys.exit(1)
        if locations_id[0] == depot_id:
            location = Location(depot_id, "d", locations_x[0],
                                locations_y[0], locations_demand[0])
            parameters.LOCATIONS.insert(position, location)
            position += 1
        for s in stations:
            index = locations_id.index(s)
            location = Location(locations_id[index], "s", locations_x[index],
                                locations_y[index], 0)
            parameters.STATIONS.append(position)
            parameters.LOCATIONS.insert(position, location)
            position += 1
        for c in locations_id:
            if c != depot_id and c not in stations:
                index = locations_id.index(c)
                location = Location(locations_id[index], "c",
                                    locations_x[index], locations_y[index],
                                    locations_demand[index])
                parameters.LOCATIONS.insert(position, location)
                parameters.CUSTOMERS.append(position)
                position += 1
        self.make_distance_matrix()
