#https://stackoverflow.com/questions/1904351/python-observer-pattern-examples-tips
from observer import Observer


class Event:
    def __init__(self, name, data, autofire=True):
        self.name = name
        self.data = data
        if autofire:
            self.fire()

    def fire(self):
        for observer in Observer.observers:
            if self.name in observer.observables:
                observer.observables[self.name](self.data)
