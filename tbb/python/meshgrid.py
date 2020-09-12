import numpy as np
import matplotlib.pyplot as plt
import time

def test_draw():
    points = [
        (1, 1),
        (2, 2),
        (3, 3),
        (100, 100),
    ]
    x = list(map(lambda x: x[0], points))
    y = list(map(lambda x: x[1], points))
    plt.scatter(x, y)
    plt.grid(True)
    plt.show()


def show_grid(config, arr):
    width = config[0]
    height = config[1]
    row = []
    points = []
    for i in range(len(arr)):
        x = i % width
        y = i / width
        row.append(arr[i])
        if x == width - 1:
            points.append(row)  
            row = []
    points = np.add(points, 1)
    points = points % 2
    plt.imshow(points, origin='upper', cmap=plt.cm.gray, interpolation='nearest')
    plt.show()    

def test():
    data = [
    [0,0,0,0,0,1,1,1,1,0],
    [0,0,0,0,0,1,0,0,1,0],
    [0,0,1,0,1,0,1,1,0,0],
    [0,0,1,0,0,1,1,0,1,0],
    [0,0,1,0,1,0,0,1,1,0],
    [1,0,0,1,0,1,0,0,1,0],
    [0,1,0,0,0,1,1,1,1,1],
    [0,1,0,0,0,0,1,1,1,1],
    [1,0,0,0,1,1,1,0,1,0],
    [1,1,1,1,0,0,0,1,1,0]
    ]
    data = np.add(data, 1)
    data = data % 2
    plt.imshow(data, origin='upper', cmap=plt.cm.gray, interpolation='nearest')
    plt.show()    

class world:
    def __init__(this, width, height):
        this.width = width
        this.height = height
        this.arr = [0]*(width*height)
        this.arr[0] = 1
        this.arr[width] = 1
        this.arr[width * height - 1] = 1

def draw_world(_world):
    show_grid((_world.width, _world.height), _world.arr)

def init():
    return

if __name__ == "__main__":
    #show_grid((3, 2), [1,0,0,1,1,1])
    #test()
    a = world(100, 100)
    draw_world(a)
    
    pass