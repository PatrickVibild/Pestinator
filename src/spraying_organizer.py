from observer import Observer
from fieldgenerator import FieldGenerator

class Spraying_Organizer(Observer):
    def __init__(self, world: FieldGenerator):
        Observer.__init__(self)
        self.observe('sick_plant', self.add_sick_plant)
        self.sick_plants = [[0 for c in range(world.i)] for r in range(world.j)]
        self.sick_coordinate_list = []

    def add_sick_plant(self, coordinates):
        i, j = coordinates
        self.sick_plants[i][j] = 1
        if coordinates not in self.sick_coordinate_list:
            #print('Sick crop received: {0}, {1}'.format(str(i), str(j)))
            self.sick_coordinate_list.append(coordinates)