import numpy as np

from cube import Cube, Preview

cube = Cube()
preview = Preview()

preview.set_camera((9.0, 7.0, 5.0))

for layer, sign in zip(np.random.randint(0, 9, 100), np.random.choice([-1.0, 1.0], 100)):
    for i in range(15):
        cube.rotate(layer, sign * np.pi / 2.0 / 15)
        preview.show(cube.state)
