from PIL import Image, ImageDraw
from random import randint
import math

ColorTable = {}
ColorTable[0] = (255, 0, 0) 
ColorTable[1] = (0, 255, 0) 
ColorTable[2] = (0, 0, 255) 
ColorTable[3] = (0, 0, 0) 


class Point(object):
    __radius = 4
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, draw):
        draw.ellipse((self.x - Point.__radius, self.y - Point.__radius) + (self.x + Point.__radius, self.y + Point.__radius), ColorTable[self.color])

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

def generateRandomMap(width, height, N):
    result = Map()
    for i in range(N):
        x, y = randint(0, width), randint(0, height)
        p = Point(x, y, 0)
        result.points.append(p)
    while True:
        added = False
        for i in range(N):
            nearest_distance = 10000
            nearest_point = None
            p1 = result.points[i]
            for j in range(N):
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

def main():
    im = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    #draw.line((0, 0) + im.size, fill=128)
    m = generateRandomMap(400, 400, 6)
    m.draw(draw)
    im.show()

if __name__ == '__main__':
    main()