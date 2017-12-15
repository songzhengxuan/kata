from PIL import Image, ImageDraw
from random import randint
import math
import sys
import time
from mapgraph import Map
import mapgraph
from mapcolor import MapColor
import InferenceBacktracking

def meaure_time(func):
    def wrapper(*args, **kargs):
        start = time.clock()
        func(*args, **kargs)
        end = time.clock();
        print("%s take %f" % (func.__name__, (end - start)))
    return wrapper

@meaure_time
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

        minConfilitCount = sys.maxsize
        minConflictColor = 0
        for color, conflict in conflictCount.items():
            if conflict < minConfilitCount:
                minConfilitCount = conflict
                minConflictColor = color
        randomPoint.color = minConflictColor
    # end of for max loop

def isValidMap(_map):
    '''
    判断是不是所有的点都已经上色，而且符合不冲突的条件
    '''
    for e in _map.edges:
        h, t = e.start, e.end
        if h.color != 0 and t.color != 0 and h.color != t.color:
            continue
        else:
            return False
    return True

def solve_use_forward_checking(_map):
    solver = MapColor(_map, 4)
    InferenceBacktracking.backtracking_search(solver)

def main():
    '''
    main func
    '''
    im = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    #draw.line((0, 0) + im.size, fill=128)
    m = mapgraph.generateRandomMap(400, 400, 64)
    print(isValidMap(m))
    #minConflict(m, 4, 1000)
    solve_use_forward_checking(m)
    print(isValidMap(m))
    m.draw(draw)
    im.show()

if __name__ == '__main__':
    main()
