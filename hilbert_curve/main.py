'''
Python adaptation of the C code found on https://en.wikipedia.org/wiki/Hilbert_curve, visualized with Pyglet
'''



def xy2d(n, x, y):
    d = 0
    s = n // 2
    while s > 0:
        rx = (x & s) > 0
        ry = (y & s) > 0
        d += s*s * ((3 * rx) ^ ry)
        x, y = rot(s, x, y, rx, ry)
        s //= 2

    return d



def d2xy(n, d):
    t = d
    x = y = 0

    s = 1
    while s < n:
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        x, y = rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2

    return x, y



def rot(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x = n-1 - x
            y = n-1 - y
        
        # Reverse order instead of swapping
        return y, x 

    return x, y



if False: # Set to true to enable jit-compilation
    import numba as nb
    xy2d = nb.njit(xy2d, cache=True)
    d2xy = nb.njit(d2xy, cache=True)
    rot  = nb.njit(rot,  cache=True)

if __name__ == "__main__":
    import pyglet as pgl
    from pyglet.gl import GL_LINES, GL_POINTS, glPointSize

    import numpy as np
    
    from time import perf_counter as pc

    res = (540, 540)
    from pyglet.window import Window
    
    win = pgl.window.Window(*res)

    def generate_hilbert_curve(n):
        # Choose distance between points based on resolution and number of points
        point_dist = res[0] / np.sqrt(n)
        offset = point_dist / 2

        # Generate points following the Hilbert curve with d in [0, n]
        points = np.array([t for d in range(n) for t in d2xy(n, int(d))], dtype=np.float32)
        points *= point_dist
        points += offset

        # Chain every consecutive pair of points
        lines = np.array([t for i in range(0, len(points), 2) for t in points[i:i+4]])
        line_colors = np.random.randint(0, 255, int(len(lines) * 3/2))

        point_vl = pgl.graphics.vertex_list(len(points)//2, ("v2f", points))
        line_vl  = pgl.graphics.vertex_list(len(lines)//2 , ("v2f", lines), ("c3B", line_colors))

        return point_vl, line_vl

    global n
    n = 1

    global on_draw
    @win.event
    def on_draw():
        win.clear()
        
        global n
        point_vl, line_vl = generate_hilbert_curve(n)
        
        point_vl.draw(GL_POINTS)
        line_vl.draw(GL_LINES)
        
        # Limit n to a reasonable value
        if n < 2**8:
            n *= 4

    glPointSize(5)
    update = lambda dt: on_draw
    pgl.clock.schedule_interval(update, 1)
    pgl.app.run()