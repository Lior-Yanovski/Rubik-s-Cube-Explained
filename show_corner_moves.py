import numpy as np

from cube import Cube, Preview

cube = Cube()
preview = Preview()

preview.set_camera((9.0, 7.0, 5.0))


def do_c_move():
    for i in range(20):
        cube.rotate(2, -np.pi / 2.0 / 20)
        preview.show(cube.state)
    for i in range(20):
        cube.rotate(5, np.pi / 2.0 / 20)
        preview.show(cube.state)
    for i in range(20):
        cube.rotate(2, np.pi / 2.0 / 20)
        preview.show(cube.state)
    for i in range(20):
        cube.rotate(5, -np.pi / 2.0 / 20)
        preview.show(cube.state)


colors = cube.colors.copy()
selection = [17, 23, 25]
subset = [i for i in range(27) if i not in selection]
cube.colors[subset, 1:] = [0.1, 0.1, 0.1, 1.0]
cube.colors[17, 1:] = [0.0, 0.058187179267406464, 0.4259052872657776, 1.0],
cube.colors[23, 1:] = [0.0, 0.3344578146934509, 0.06190747395157814, 1.0],
cube.colors[25, 1:] = [0.4819522500038147, 0.002932318253442645, 0.030256519094109535, 1.0]

for i in range(60):
    preview.show(cube.state)

do_c_move()
do_c_move()
do_c_move()

for i in range(60):
    preview.show(cube.state)
