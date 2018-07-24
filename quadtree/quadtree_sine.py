 #!/usr/bin/env python
import numpy as np

import pyglet as pgl
from pyglet.gl import *

from time import perf_counter_ns as ns

class Quadtree:

    def __init__(self, center_x, center_y, halfsize):
        self.center_x = center_x
        self.center_y = center_y
        self.halfsize = halfsize

        self.NW = None; self.NE = None
        self.SW = None; self.SE = None
    
        # x is  -1 if no point is set
        #       -2 if the tree is subdivided
        #      >=0 otherwise

        self.x, self.y = -1, -1

    
    def isSubdivided(self):
        return self.x == -2
    
    def hasPoint(self):
        return self.x >= 0

def _insert(self, x, y):
    if y > self.center_y:
        if x < self.center_x:
            insert_point(self.NW, x, y)
        else:
            insert_point(self.NE, x, y)
    else:
        if x < self.center_x:
            insert_point(self.SW, x, y)
        else:
            insert_point(self.SE, x, y)

def insert_point(self, x, y):
    '''Insert a point into the quadtree.
    '''
    if not self.hasPoint() and not self.isSubdivided():
        self.x = x
        self.y = y

    elif self.isSubdivided():
        _insert(self, x, y)

    else:
        cx, cy = self.center_x, self.center_y
        qs = self.halfsize / 2

        self.NW = Quadtree(cx - qs, cy + qs, qs)
        self.NE = Quadtree(cx + qs, cy + qs, qs)
        self.SW = Quadtree(cx - qs, cy - qs, qs)
        self.SE = Quadtree(cx + qs, cy - qs, qs)

        _insert(self, self.x, self.y)
        _insert(self, x, y)

        self.x = -2
        self.y = -2


def level_to_color(level):
    return [40*level, 96, 128 - 4*level, 40*level, 96, 128 - 4*level]

def dive_tree(tree: Quadtree, level, lines, line_colors, points):
    '''Performs a DFS-style dive through the quadtree, adding
    found points and lines used for quadrant visualization.
    '''

    if tree.isSubdivided():
        cx, cy = tree.center_x, tree.center_y
        hs = tree.halfsize

        l1 = (cx - hs, cy, cx + hs, cy) # Horizontal line
        l2 = (cx, cy + hs, cx, cy - hs) # Vertical line

        lines.extend(l1)
        lines.extend(l2)

        color = level_to_color(level)
        line_colors.extend(color)
        line_colors.extend(color)

        dive_tree(tree.NW, level+1, lines, line_colors, points)
        dive_tree(tree.NE, level+1, lines, line_colors, points)
        dive_tree(tree.SW, level+1, lines, line_colors, points)
        dive_tree(tree.SE, level+1, lines, line_colors, points)
    
    elif tree.hasPoint():
        points.extend((tree.x, tree.y))

res = np.array([840, 480])

num_points = 400

center_x = res[0] / 2
center_y = res[1] / 2
halfsize = res[0] / 2

#point_colors = np.random.randint(0, 255, 3*num_points)
point_colors = (192, 192, 192) * num_points

global line_vl
line_vl = pgl.graphics.vertex_list(0, "v2f")
point_vl = pgl.graphics.vertex_list(num_points, "v2f", ("c3B", point_colors))

win = pgl.window.Window(*res)

glEnable(GL_POINT_SMOOTH)
glPointSize(2)

def recalc(t):
    tree = Quadtree(center_x, center_y, halfsize)

    xs = np.linspace(0, res[0], num_points)
    ys = (res[1]/4) * np.sin(1/(84 + 48 * np.sin(t/60)) * (xs)) + res[1]/2

    for x, y in zip(xs, ys):
        insert_point(tree, x, y)

    lines = []
    line_colors = []
    points = []

    st = ns()
    dive_tree(tree, 0, lines, line_colors, points)
    et = ns()
    print("Dive time:", (et-st)/1e6, "ms")

    point_vl.vertices = points
    global line_vl
    line_vl = pgl.graphics.vertex_list(len(lines) // 2, ("v2f", lines), ("c3B", line_colors))


@win.event
def on_draw():
    win.clear()
    line_vl.draw(GL_LINES)
    point_vl.draw(GL_POINTS)

global t
t = 0
def update(dt):
    global t
    t += dt * 90
    recalc(t)
    on_draw()

recalc(0)
pgl.clock.schedule_interval(update, 1/144)
pgl.app.run()