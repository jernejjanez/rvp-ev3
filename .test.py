import calc_distances
import json
import copy
def get_locations(file='zemljevid.json'):
    # read file
    with open(file, 'r') as data:
        return json.load(data)

t = calc_distances.CalcDistances(get_locations())
#current_coords = 
#current_coords.x += 5
print("start",t.start)
#print("cc",current_coords)
print(t.next_person.coords)
t.check_as_visited()
print([p.checked for p in t.persons])