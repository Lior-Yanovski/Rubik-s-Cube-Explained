import pyglet

pyglet.options['shadow_window'] = False
pyglet.options['debug_gl'] = False


class Window(pyglet.window.Window):
    def __init__(self, width, height):
        self.time = 0.0
        self.alive = True
        self.mouse = (0, 0)
        self.keys_pressed = set()
        self.keys = set()
        config = pyglet.gl.Config(
            major_version=3,
            minor_version=3,
            forward_compatible=True,
            double_buffer=False,
            depth_size=0,
            samples=0,
        )
        super().__init__(width=width, height=height, config=config, vsync=True)
        width, height = self.get_framebuffer_size()
        self.size = (width, height)
        self.aspect = width / height
        # self.set_location(100, 100)

    def on_resize(self, width, height):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, symbol, modifiers):
        self.keys_pressed.add(symbol)
        self.keys.add(symbol)

    def on_key_release(self, symbol, modifiers):
        self.keys.discard(symbol)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse = (x, y)

    def on_close(self):
        self.alive = False

    def update(self):
        self.keys_pressed.clear()
        self.flip()
        self.dispatch_events()
        self.time += 1.0 / 60.0
        return self.alive
