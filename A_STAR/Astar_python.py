# Program to read in a map text file and print info.

import math
import sys
from pqueue import PQueue
import argparse
import time

class Location(object):
        def __init__(self, id, lat, lon):
                self.id = id;
                self.lat = lat;
                self.lon = lon;
                
class Road(object):
        def __init__(self, start_id, end_id, name, max_speed):
                self.start_id = start_id
                self.end_id = end_id
                self.name = name
                self.max_speed = max_speed
class Node(object):
        def __init__(self, id, lat, lon, f, g, h):
                self.id = id
                self.lat = lat
                self.lon = lon
                self.f = f
                self.g = g
                self.h = h
        
class Graph(object):
        def __init__(self):
                self.locations = {}
                self.roads = {}
                
        def add_location(self, id, lat, lon):
                loc = Location(id, lat, lon)
                self.locations[id] = loc # insert into dictionary
                # now we can look up any location by its ID
                
        def add_road(self, start_id, end_id, name, speed):
                rd = Road(start_id, end_id, name, speed)
                
                # first road seen from start_id?
                if start_id not in self.roads:
                        self.roads[start_id] = [ rd ] # insert new list into dictionary
                else:
                        self.roads[start_id].append(rd)

        def get_location(self, id):
                return self.locations[id]                       

        def get_roads(self, id):
                return self.roads[id]
        
def main():
        #parser = argparse.ArgumentParser()
        #parser.add_argument('file')
        #parser.add_argument('start')
        #parser.add_argument('end')

        #args = parser.parse_args()

        filename = "a.txt"
        g = read_graph(filename)
        
        while True:
                #id = int(args.start)
                #id2 = int(args.end)
                id = int(input("\nEnter a starting location or zero to quit: "))
                if id == 0: break
                frontier = PQueue()
                id2 = int(input("\nEnter a ending location or zero to quit: "))
                if id2 == 0: break
                print("Routing from ", id, " to ", id2)
                l1 = g.get_location(id)
                l2 = g.get_location(id2)
                gv = 0
                hv = 65
                fv = gv+hv
                #print ("Starting Location is lat:  ", l1.lat, " long: ", l1.lon)
                explored = []
                ordered = {}
                final = [id]
                #print (ordered[0].lat)
                rds = g.get_roads(id)
                rds2 = g.get_roads(id2)
                frontier.enqueue(l1.id,fv)
                #print("Location", id, "has roads leading to:")
                #for rd in rds:
                        #print(" ", rd.end_id, rd.max_speed, "mph", rd.name)

                #print("Location", id2, "has roads leading to:")
                #for rd in rds2:
                        #print(" ", rd.end_id, rd.max_speed, "mph", rd.name)
                done = False
                while not frontier.empty() and not done:
                        p = frontier.dequeue()
                        if (p == id2):
                                print("Number of nodes expanded; ", len(explored))
                                print("The path found: ")
                                print(p)
                                done = True
                                #loop thru
                                parent = ordered[p]
                                #final.insert[id]
                                while parent != id:
                                        print(parent)
                                        parent = ordered[parent]

                                print(id)

                                break

                        explored.append(p)
                        rds3 = g.get_roads(p)
                        # print("Location", p, "has roads leading to:")
                        # for rd in rds3:
                                # print(" ", rd.end_id, rd.max_speed, "mph", rd.name)

                        # print("EXPLEORED", len(explored), str(explored))
                        for rd in rds3:

                                rdloc = g.get_location(rd.end_id)
                                gv = distance(l1.lat, l1.lon, rdloc.lat, rdloc.lon)
                                hv = distance(rdloc.lat, rdloc.lon, l2.lat, l2.lon)
                                h = (hv)*60/65
                                dg = (gv)*60/rd.max_speed
                                f = h+dg
                                #print(rd.start_id," ", rd.end_id, rd.max_speed, "mph", rd.name)
                                print("Visiting", rd.start_id, " ",rd.end_id," ",rd.end_id, " g=",dg, " h=",h," f=",f,)


                                f_cont = frontier.contains(rd.end_id)
                                if (rdloc.id not in explored and f_cont == False):
                                        ordered[rdloc.id] = p
                                        frontier.enqueue(rdloc.id,f)
                                        print("   Adding ",rdloc.id, " g=",dg, " h=",h," f=",f, " to frontier")
                                elif (f_cont == True and f < frontier.get_priority(rdloc.id)):
                                        ordered[rdloc.id] = p
                                        frontier.change_priority(rdloc.id,f)


        
def read_graph(filename):
        try:
                file = open(filename, "r")
        except:
                print("Bad filename")
                return None
                
        g = Graph()
        for line in file:
                pieces = line.strip().split("|")
                
                if pieces[0] == "location":
                        id = int(pieces[1])
                        longitude = float(pieces[2])
                        latitude = float(pieces[3])
                        g.add_location(id, latitude, longitude)
                        
                elif pieces[0] == "road":
                        start = int(pieces[1])
                        end = int(pieces[2])
                        speed = int(pieces[3])
                        name = pieces[4]
                        g.add_road(start, end, name, speed)
                        g.add_road(end, start, name, speed)
                        
        return g
def distance(lat1, long1, lat2, long2):
        # Convert latitude and longitude to
        # spherical coordinates in radians.
        if lat1==lat2 and long1==long2: return 0
        degrees_to_radians = math.pi/180.0
        # phi = 90 - latitude
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians
        # theta = longitude
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians
        # Compute spherical distance from spherical coordinates.
        # For two locations in spherical coordinates
        # (1, theta, phi) and (1, theta', phi')
        # cosine( arc length ) =
        # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
        math.cos(phi1)*math.cos(phi2))
        # print (cos)
        arc = math.acos( cos )
        arc = arc*3960
        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length.
        return arc      

main()
