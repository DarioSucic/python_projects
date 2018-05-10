# Prims algorithm with euclidean distance
import numpy as np
import numba as nb

@nb.njit
def pindx(index):
    return 2 * index

@nb.njit
def euclidean(a, _i, _j):
    # Euclidean distance between points _i and _j
    return (a[_j]-a[_i])**2 + (a[_j+1]-a[_i+1])**2

@nb.njit
def prim(a):
    # Prim's algorithm with euclidean distance

    n = a.size // 2
    m = np.zeros((n, n), dtype=np.uint8)

    INF = 2**31 - 1
    c = np.zeros(n, dtype=np.uint8)
    c[0] = 1

    for _ in range(n-1):
        ii, jj = -1, -1
        d = INF

        for i in range(n):
            if not c[i]:
                continue
            _i = pindx(i)
            for j in range(n):
                if c[j] or m[i, j] or m[j, i] or i == j:
                    continue
                _j = pindx(j)
                pdist = euclidean(a, _i, _j)
                if pdist < d:
                    ii, jj = i, j
                    d = pdist

        m[ii, jj] = 1
        c[jj] = 1
    
    return m


if __name__ == "__main__":
    import pyglet as pgl
    from pyglet.gl import *

    res = (640, 640)
    win = pgl.window.Window(*res)

    n = 16 # Number of points
    points = np.random.randint(40, res[0] - 40, size=2*n, dtype=np.uint16)
    m = prim(points) # Neighbourhood matrix

    p = points
    lines = np.empty(4*(n-1), dtype=np.uint16) # n-1 lines for n points
    colors = np.random.randint(0, 255, 6*(n-1), dtype=np.uint8)
    labels = pgl.graphics.Batch()

    n = m.shape[0]
    c = 0
    for i in range(n):
        for j in range(n):
            if m[i, j]:
                _i = pindx(i)
                _j = pindx(j)
                lines[c:c+4] = [p[_i], p[_i+1], p[_j], p[_j+1]]
                c += 4

                x = (p[_j] + p[_i]) / 2
                y = (p[_j+1] + p[_i+1]) / 2
                #pgl.text.Label(f"{i},{j}", x=x, y=y, batch=labels)
                

    vl_points = pgl.graphics.vertex_list(len(points) // 2, ("v2i/static", points))
    vl_lines  = pgl.graphics.vertex_list(len(lines) // 2, ("v2i/static", lines), ("c3B/static", colors))

    @win.event
    def on_draw():
        vl_points.draw(GL_POINTS)
        vl_lines.draw(GL_LINES)
        #labels.draw()
    
    glPointSize(4)
    pgl.app.run()
