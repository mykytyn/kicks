import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time

def run_simulation(numCircs=100):
    def calc_collisions(circle, circles, wrap=False):
        toMove = []
        cent1 = circle.center
        radius = circle.get_radius()
        distcomp = 4 * radius * radius
        halfx = x1*.5
        halfy = x1*.5
        for k in range(len(circles)):
            if circle == circles[k]:
                continue
            cent2 = circles[k].center
            dx = cent1[0]-cent2[0]
            dy = cent1[1]-cent2[1]
            if wrap:
                if np.abs(dx) > halfx:
                    dx = dx - np.copysign(x1, dx)
                if np.abs(dy) > halfy:
                    dy = dy - np.copysign(y1, dy)
            if (dx * dx + dy * dy) <= distcomp:
                toMove.append(circle)
                toMove.append(circles[k])
                continue
        return toMove

    
    def move_circle(circle):
        a = int(circle.center[0] / boxsize)
        b = int(circle.center[1] / boxsize)
        movex = (np.random.rand() - 1 / 2.) * 2. * epsilon
        movey = (np.random.rand() - 1 / 2.) * 2. * epsilon
        xpos = circle.center[0] + movex
        ypos = circle.center[1] + movey
        if xpos >= x1:
            xpos = xpos - x1
        if ypos >= y1:
            ypos = ypos - y1
        if xpos <= x0:
            xpos = x1 + xpos
        if ypos <= y0:
            ypos = y1 + ypos
        circle.center = (xpos, ypos)
        a2 = int(circle.center[0] / boxsize)
        b2 = int(circle.center[1] / boxsize)
        if a != a2 or b != b2:
            boxes[a][b].remove(circle)
            boxes[a2][b2].append(circle)


    def run_once():
        oldMove = circles
        for i in range(numSteps):
            toMove = []
            for circ in oldMove:
                if plot:
                    circ.set_fc('blue')
                a = int(circ.center[0] / boxsize)
                b = int(circ.center[1] / boxsize)
                targets = []
                wrap = False
                if a == 0:
                    aa = [len(boxes) - 1, a, a + 1]
                    wrap = True
                elif a == len(boxes) - 1:
                    aa = [a - 1, a, 0]
                    wrap = True
                else:
                    aa = [a - 1, a, a + 1]
                if b == 0:
                    bb = [len(boxes) - 1, b, b + 1]
                    wrap = True
                elif b == len(boxes) - 1:
                    bb = [b - 1, b, 0]
                    wrap = True
                else:
                    bb = [b - 1, b, b + 1]
                for x in aa:
                    for y in bb:
                        targets.extend(boxes[x][y])
                toMove.extend(calc_collisions(circ, targets, wrap))
            for j in set(toMove):
                move_circle(j)
                if plot:
                    j.set_fc('red')
            if len(toMove) == 0:
                break
            if plot:
                if i%stepsize == 0:
                    plt.show()
            oldMove = list(set(toMove))
        return i
    plot = False
    if plot:
        plt.ion()
        fig = plt.figure(figsize=(8,8))

    numSteps = 400000
    x0 = 0.
    x1 = 100
    y0 = 0.
    y1 = 100
    radius = 1.
    epsilon = .5 * radius
    stepsize = 10
    divisor = x1 / (2 * radius)
    boxsize = x1 / divisor

    boxsize = int(boxsize)
    circles = []
    boxes = [[[] for i in range(x1 / boxsize)] for j in range(y1 / boxsize)]

    for i in range(numCircs):
        xpos = np.random.rand() * (x1 - x0)
        ypos = np.random.rand() * (y1 - y0)
        circle = plt.Circle((xpos, ypos), radius=radius)
        boxx = int(xpos / boxsize)
        boxy = int(ypos / boxsize)
        boxes[boxx][boxy].append(circle)
        circles.append(circle)
        if plot:
            fig.gca().add_artist(circle)
    if plot:
        plt.xlim((x0,x1))
        plt.ylim((y0,y1))
        plt.show()
    
    distcomp = 4 * radius * radius

    total_steps = []
    for j in range(25):
        total_steps.append(run_once())
        for circ in circles:
            move_circle(circ)
            circ.set_fc('red')
        if plot:
            plt.show()
    print total_steps
    return total_steps

            
if __name__ == '__main__':
    f = open('first_sim.txt','w')
    steps = [1300]*10
    pool = Pool(processes=10)
    steps = pool.map(run_simulation,steps)
    f.write(str(steps))
    f.close()
