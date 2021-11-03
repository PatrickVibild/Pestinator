import fastrand
import numpy
import threading
from observer import Observer


def crop_color(infection: float):
    if infection < 0.2:
        return (0, 255, 0)
    if infection < 0.6:
        return (255, 165, 0)
    if infection < 0.95:
        return (255, 0, 0)
    return (255, 255, 255)


class FieldGenerator(Observer):
    def __init__(self, i, j, initial_infection=0.01):
        Observer.__init__(self)
        self.observe('spray', self.cure) # Listening to events 'spray' and calling method cure if trigger
        self.i = i
        self.j = j
        self.field = [[CropCell(fastrand.pcg32bounded(10000) / 10000) for x in range(i)] for y in range(j)]
        self.image = numpy.zeros((self.i * 6, self.j * 6, 3))

    def render(self):
        while True:
            for y in range(self.j):
                for x in range(self.i):
                    cell_color = crop_color(self.field[x][y].infection)
                    for n in range(6):
                        for m in range(6):
                            self.image[(x * 6) + n][(y * 6) + m] = cell_color

    def run(self):
        t1 = threading.Thread(target=self.render)
        t1.start()

    def cure(self, coordinates):
        x, y = coordinates
        print('Cleaning crop{0}, {1}'.format(str(x), str(y)))
        self.field[x][y].infection = 0.0
        print('a')


class CropCell:
    def __init__(self, infection):
        assert infection <= 1
        assert infection >= 0
        self.infection = infection
        self.alive = True

    def is_sick(self):
        if not self.alive or self.infection <= 0.2:
            return False
        return True

    # TODO - implement cell update from its neightbours.
    def update(self):
        self.alive = False if self.infection > 0.95 else True
