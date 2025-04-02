import pyglet

class Game:
    def __init__(self, window):
        self.window = window
        self.current_scene = None

    def switch_scene(self, scene):
        self.current_scene = scene
        pyglet.clock.unschedule(self.current_scene.update)
        pyglet.clock.schedule_interval(scene.update, 1/60.0)  # 60 FPS

    def on_draw(self):
        if self.current_scene:
            self.current_scene.on_draw()

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)