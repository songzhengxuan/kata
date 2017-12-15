'''
common graph class and function defination
'''
import sys
import math
from random import randint

ColorTable = {}
ColorTable[0] = (0, 0, 0) 
ColorTable[1] = (0, 255, 0) 
ColorTable[2] = (0, 0, 255) 
ColorTable[3] = (255, 0, 0) 
ColorTable[4] = (255, 255, 0)

class Point(object):
    __radius = 4
    
    def __init__(self, x, y, color): #pylint disable
        self.x = x
        self.y = y
        self.color = color
        self.edges = None

    def draw(self, draw):
        draw.ellipse((self.x - Point.__radius, self.y - Point.__radius) + (self.x + Point.__radius, self.y + Point.__radius), ColorTable[self.color])
    
    def reset(self):
        self.color = 0
    
    def addEdge(self, edge):
        if self.edges is None:
            self.edges = edge
            edge.next = None
        else:
            edge.next = self.edges
            self.edges = edge

    def isConnectedTo(self, otherPoint):
        e = self.edges
        while e is not None:
            if e.end == otherPoint:
                return True
            e = e.next
        return False

class Edge(object): #pylint disable
    '''
    Link list node for edge
    '''
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.next = None



class Map(object):
    def __init__(self):
        self.points=[]
        self.edges=[]
    
    def draw(self, imageDraw):
        for p in self.points:
            p.draw(imageDraw)
        for e in self.edges:
            start, end = e.start, e.end
            imageDraw.line((start.x, start.y) + (end.x, end.y), fill=128)

    def connect(self, p1, p2):
        edge1 = Edge(p1, p2)
        p1.addEdge(edge1)
        edge2 = Edge(p2, p1)
        p2.addEdge(edge2)
        self.edges.append(edge1)
        self.edges.append(edge2)
        return edge1, edge2

    def reset(self):
        for p in self.points:
            p.reset()

def generateRandomMap(width, height, N):
    result = Map()
    for i in range(N):
        x, y = randint(0, width), randint(0, height)
        p = Point(x, y, 0)
        result.points.append(p)
    while True:
        added = False
        for i in range(N):
            nearest_distance = sys.maxsize
            nearest_point = None
            p1 = result.points[i]
            for j in range(N):
                if j == i:
                    continue
                p2 = result.points[j]
                valid = True
                if p1.isConnectedTo(p2):
                    continue
                for e in result.edges:
                    e1, e2 = e.start, e.end
                    if intersect(p1, p2, e1, e2):
                        valid = False
                        break
                if valid:
                    if line_length(p1, p2) < nearest_distance:
                        nearest_distance = line_length(p1, p2)
                        nearest_point = p2
                        
            if nearest_point != None:
                result.connect(p1, nearest_point)
                added = True

        if not added:
            break

    return result
        
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

def line_length(p1, p2):
    return math.sqrt(math.pow((p2.x - p1.x), 2) + math.pow((p2.y - p1.y), 2));

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
