
# Hilbert curve generator

---

A basic Python adaptation of the C functions from the [Hilbert_curve](https://en.wikipedia.org/wiki/Hilbert_curve) wikipedia page with a graphical representation of the result. Usable as a library.

  

**Usage**:

To run the visual demo, simply run the python file.

```cmd

python.exe main.py

```

  

```sh

python3 ./main.py

```

For library use the *xy2d* and *d2xy* can be imported.

```python

from hilbert_curve import xy2d, d2xy

```

  

**Dependencies**:

```sh

pip install numpy

pip install pyglet

```

  

Numba is also a requirement if JIT-compilation is enabled.

```sh

pip install numba

```

![demo.png](https://raw.githubusercontent.com/DarioSucic/python_projects/master/hilbert_curve/images/demo.png)
