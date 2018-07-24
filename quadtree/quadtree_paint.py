 #!/usr/bin/env python
import numpy as np

import pyglet as pgl
import pyglet.window.mouse as mb
from pyglet.gl import *

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
    return (int(255/10 * level), 96 - level, 128 - 4 * level)



def dive_tree(tree: Quadtree, level, lines, line_colors, points, point_colors):
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

        color = level_to_color(level) * 2
        line_colors.extend(color)
        line_colors.extend(color)

        dive_tree(tree.NW, level+1, lines, line_colors, points, point_colors)
        dive_tree(tree.NE, level+1, lines, line_colors, points, point_colors)
        dive_tree(tree.SW, level+1, lines, line_colors, points, point_colors)
        dive_tree(tree.SE, level+1, lines, line_colors, points, point_colors)
    
    elif tree.hasPoint():
        points.extend((tree.x, tree.y))
        point_colors.extend(level_to_color(level))



res = np.array([840, 840])

center_x = res[0] / 2
center_y = res[1] / 2
halfsize = res[0] / 2

global line_vl, point_vl
line_vl = pgl.graphics.vertex_list(0, "v2f", "c3B")
point_vl = pgl.graphics.vertex_list(0, "v2f", "c3B")

win = pgl.window.Window(*res)

glEnable(GL_POINT_SMOOTH)
glPointSize(3)

tree = Quadtree(center_x, center_y, halfsize)

def recalc():
    lines = []
    line_colors = []
    points = []
    point_colors = []

    dive_tree(tree, 0, lines, line_colors, points, point_colors)
    global line_vl, point_vl
    line_vl = pgl.graphics.vertex_list(len(lines) // 2, ("v2f", lines), ("c3B", line_colors))
    point_vl = pgl.graphics.vertex_list(len(points) // 2, ("v2f", points), ("c3B", point_colors))

@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mb.LEFT:
        insert_point(tree, x, y)

@win.event
def on_mouse_press(x, y, buttons, modifiers):
    on_mouse_drag(x, y, 0, 0, buttons, modifiers)

@win.event
def on_draw():
    win.clear()
    recalc()
    line_vl.draw(GL_LINES)
    point_vl.draw(GL_POINTS)

pgl.app.run()