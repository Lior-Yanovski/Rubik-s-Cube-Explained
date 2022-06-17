import numpy as np

from cube import Cube, Preview

cube = Cube()
preview = Preview()

preview.set_camera((9.0, 7.0, 5.0))

print('This is the Rubik\'s Cube')

for i in range(120):
    preview.show(cube.state)

print('Rotating the red face clockwise is the "R" move')

for i in range(240):
    preview.show(cube.state)

for i in range(30):
    cube.rotate(2, -np.pi / 2.0 / 30)
    preview.show(cube.state)

print('Rotating the red face counter-clockwise is the inverse of the "R" move')

for i in range(240):
    preview.show(cube.state)

for i in range(30):
    cube.rotate(2, np.pi / 2.0 / 30)
    preview.show(cube.state)

print('Rotating the blue face counter-clockwise is the "B" move')

for i in range(240):
    preview.show(cube.state)

for i in range(30):
    cube.rotate(5, np.pi / 2.0 / 30)
    preview.show(cube.state)

print('Rotating the blue face clockwise is the inverse of the "B" move')

for i in range(240):
    preview.show(cube.state)

for i in range(30):
    cube.rotate(5, -np.pi / 2.0 / 30)
    preview.show(cube.state)

print('Now let us define the C move as')

for i in range(180):
    preview.show(cube.state)

print('R')

for i in range(30):
    preview.show(cube.state)

for i in range(30):
    cube.rotate(2, -np.pi / 2.0 / 30)
    preview.show(cube.state)

for i in range(30):
    preview.show(cube.state)

print('B')

for i in range(30):
    preview.show(cube.state)

for i in range(30):
    cube.rotate(5, np.pi / 2.0 / 30)
    preview.show(cube.state)

for i in range(30):
    preview.show(cube.state)

print('R^-1')

for i in range(30):
    preview.show(cube.state)

for i in range(30):
    cube.rotate(2, np.pi / 2.0 / 30)
    preview.show(cube.state)

for i in range(30):
    preview.show(cube.state)

print('B^-1')

for i in range(30):
    preview.show(cube.state)

for i in range(30):
    cube.rotate(5, -np.pi / 2.0 / 30)
    preview.show(cube.state)

for i in range(30):
    preview.show(cube.state)

print('As you can see the C move ...')

for i in range(180):
    preview.show(cube.state)

colors = cube.colors.copy()

for i in range(30):
    subset = [i for i in range(27) if i not in (17, 23, 25)]
    cube.colors[subset, 1:] = colors[subset, 1:] * (1.0 - i / (30 - 1)) + np.array([0.05, 0.05, 0.05, 1.0]) * i / (30 - 1)
    preview.show(cube.state)

for i in range(180):
    preview.show(cube.state)

for i in range(30):
    subset = [i for i in range(27) if i not in (17, 23, 25)]
    cube.colors[subset, 1:] = colors[subset, 1:] * i / (30 - 1) + np.array([0.05, 0.05, 0.05, 1.0]) * (1.0 - i / (30 - 1))
    preview.show(cube.state)

for i in range(180):
    preview.show(cube.state)

for i in range(30):
    subset = [i for i in range(27) if i not in (8, 20, 24, 26)]
    cube.colors[subset, 1:] = colors[subset, 1:] * (1.0 - i / (30 - 1)) + np.array([0.05, 0.05, 0.05, 1.0]) * i / (30 - 1)
    preview.show(cube.state)

for i in range(180):
    preview.show(cube.state)

for i in range(30):
    subset = [i for i in range(27) if i not in (8, 20, 24, 26)]
    cube.colors[subset, 1:] = colors[subset, 1:] * i / (30 - 1) + np.array([0.05, 0.05, 0.05, 1.0]) * (1.0 - i / (30 - 1))
    preview.show(cube.state)

cube.colors[:] = colors

for i in range(180):
    preview.show(cube.state)
