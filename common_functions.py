import math

def distance_finder(loc1, loc2):
    inside = ((loc1[0] - (loc2[0])) ** 2) + ((loc1[1] - (loc2[1])) ** 2) + ((loc1[2] - (loc2[2])) ** 2)
    distance = math.sqrt(inside)
    distance = round(distance, 2)
    return distance