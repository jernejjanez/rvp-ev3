import math

class Coordinates:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def calculate_distance(self, coords):
        return abs(self.x - coords.x) + abs(self.y - coords.y)
    def __str__(self):
        return "x: {}, y: {}".format(self.x,self.y)

class Person:
    def __init__(self, coords, start):
        self.coords = Coordinates(coords)
        self.checked = False
        self.distance_from_start = self.coords.calculate_distance(start)
    
    


class CalcDistances:
    def __init__(self, dictionary):
        self.start = Coordinates(dictionary["start"])
        self.persons = []
        i=1
        while 1:
            try:
                self.persons.append(Person(dictionary["oseba"+str(i)],self.start))
                i+=1
            except:
                break
        self.calculate_next(self.start) 

    def calculate_next(self, current_coords):
        distances_persons = [(current_coords.calculate_distance(p.coords),p) for p in self.persons if not p.checked]
        distances_persons_sorted = sorted(distances_persons, key=lambda tupl: tupl[0])
        if len(distances_persons_sorted):
            self.next_person = distances_persons_sorted[0][1]
            return distances_persons_sorted[0][1]
        self.next_person = None

    def check_as_visited(self):
        if self.next_person:
            self.next_person.checked = True
            self.next_person = None