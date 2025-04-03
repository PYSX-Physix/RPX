import pyglet
from pyglet.gl import GL_SRC_ALPHA, GL_ONE, glBlendFunc

class LightSource:
    def __init__(self, x, y, radius, color=(255, 255, 200), intensity=0.5):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.intensity = intensity

    def draw(self):
        light = pyglet.shapes.Circle(
            self.x, self.y, self.radius, color=self.color
        )
        light.opacity = int(self.intensity * 255)  # Convert intensity to opacity (0-255)
        light.draw()