from itertools import cycle
import numpy as np

from cube import Cube, Preview

cube = Cube()
preview = Preview()


class CursorCamera:
    def __init__(self, preview):
        self.preview = preview
        self.state = 0.5, 0.4, 12.0, 0.95

    def update(self):
        mx, my = self.preview.window.mouse
        h, v, r, f = self.state
        h = h * f + ((mx - 500) * 0.005) * (1.0 - f)
        v = v * f + np.clip((my - 360) * 0.005, -np.pi * 0.49, np.pi * 0.49) * (1.0 - f)
        self.preview.set_camera((np.cos(h) * np.cos(v) * r, np.sin(h) * np.cos(v) * r, np.sin(v) * r))
        self.state = h, v, r, f


cursor_camera = CursorCamera(preview)

t = np.sin(np.linspace(0.0, np.pi, 15))
t = t / np.sum(t) * np.pi / 2.0

cmove = cycle([(2, -1.0), (5, 1.0), (2, 1.0), (5, -1.0)])
transparent = False

while True:
    cursor_camera.update()
    preview.show(cube.state, transparent)

    if ord('q') in preview.window.keys:
        for i in range(15):
            cursor_camera.update()
            cube.rotate(8, t[i])
            preview.show(cube.state, transparent)

    if ord('w') in preview.window.keys:
        for i in range(15):
            cursor_camera.update()
            cube.rotate(7, t[i])
            preview.show(cube.state, transparent)

    if ord('e') in preview.window.keys:
        for i in range(15):
            cursor_camera.update()
            cube.rotate(6, t[i])
            preview.show(cube.state, transparent)

    if ord('z') in preview.window.keys:
        layer, sign = next(cmove)
        for i in range(15):
            cursor_camera.update()
            cube.rotate(layer, sign * t[i])
            preview.show(cube.state, transparent)

    if ord('t') in preview.window.keys_pressed:
        transparent = not transparent
