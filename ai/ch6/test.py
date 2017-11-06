from PIL import Image, ImageDraw
from random import randint
import math
import sys

ColorTable = {}
ColorTable[0] = (255, 0, 0) 
ColorTable[1] = (0, 255, 0) 
ColorTable[2] = (0, 0, 255) 
ColorTable[3] = (0, 0, 0) 
ColorTable[4] = (255, 255, 0) 


class Point(object):
    __radius = 4
    def __init__(self, x, y, color):
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

class Edge(object):
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
            nearest_distance = sys.maxint
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

def minConflict(map, maxColorCount, maxLoop):
    unassignedPoints = {}
    for i in range(maxLoop):
        if isValidMap(map):
            return
        if len(unassignedPoints) == 0:
            unassignedPoints = { p for p in map.points }

        # find a random points in un-assgined points set
        randomPoint = unassignedPoints.pop()
        conflictCount = { color : 0 for color in range(1, maxColorCount+1)}
        
        edge_to_check = randomPoint.edges
        while edge_to_check is not None:
            connect_point = edge_to_check.end
            if connect_point.color != 0:
                conflictCount[connect_point.color] += 1
            edge_to_check = edge_to_check.next

        minConfilitCount = sys.maxint 
        minConflictColor = 0
        for color, conflict in conflictCount.items():
            if conflict < minConfilitCount:
                minConfilitCount = conflict
                minConflictColor = color
        randomPoint.color = minConflictColor
    # end of for max loop

def isValidMap(map):
    for e in map.edges:
        h, t = e.start, e.end
        if h.color != 0 and t.color != 0 and h.color != t.color:
            continue
        else:
            return False
    return True

def main():
    im = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    #draw.line((0, 0) + im.size, fill=128)
    m = generateRandomMap(400, 400, 12)
    print(isValidMap(m))
    minConflict(m, 4, 1000)
    print(isValidMap(m))
    m.draw(draw)
    im.show()

if __name__ == '__main__':
    main()