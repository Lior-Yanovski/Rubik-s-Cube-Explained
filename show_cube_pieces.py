import numpy as np

from cube import Cube, Preview

cube = Cube()
preview = Preview()

preview.set_camera((9.0, 7.0, 5.0))

positions = cube.positions.copy()

for i in range(30):
    preview.show(cube.state)

for i in range(30):
    cube.positions[:] *= 1.02
    preview.show(cube.state)

for i in range(60):
    preview.show(cube.state)

for i in range(30):
    cube.positions[:] /= 1.02
    preview.show(cube.state)

for i in range(30):
    preview.show(cube.state)

cube.positions[:] = positions

for i in range(180):
    preview.show(cube.state)
