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

    def draw(self, draw):
        draw.ellipse((self.x - Point.__radius, self.y - Point.__radius) + (self.x + Point.__radius, self.y + Point.__radius), ColorTable[self.color])
    
    def reset(self):
        self.color = 0

class Map(object):
    def __init__(self):
        self.points=[]
        self.edges=[]
    
    def draw(self, imageDraw):
        for p in self.points:
            p.draw(imageDraw)
        for e in self.edges:
            start, end = e
            imageDraw.line((start.x, start.y) + (end.x, end.y), fill=128)

    def connect(self, p1, p2):
        self.edges.append((p1, p2))

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
                if (p1, p2) in result.edges or (p2, p1) in result.edges:
                    continue
                for e in result.edges:
                    e1, e2 = e
                    if intersect(p1, p2, e1, e2):
                        valid = False
                        break
                if valid:
                    if line_length(p1, p2) < nearest_distance:
                        nearest_distance = line_length(p1, p2)
                        nearest_point = p2
                        
            if nearest_point != None:
                added = True
                result.edges.append((p1, nearest_point))

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
        for edge in map.edges:
            h, t = edge
            if h == randomPoint:
                if t.color != 0:
                    conflictCount[t.color] += 1
            elif t == randomPoint:
                if h.color != 0:
                    conflictCount[h.color] += 1
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
        h, t = e
        if h.color != 0 and t.color != 0 and h.color != t.color:
            continue
        else:
            return False
    return True

def main():
    im = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    #draw.line((0, 0) + im.size, fill=128)
    m = generateRandomMap(400, 400, 6)
    print(isValidMap(m))
    minConflict(m, 4, 1000)
    print(isValidMap(m))
    m.draw(draw)
    im.show()

if __name__ == '__main__':
    main()