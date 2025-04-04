import pyglet
from pyglet.gl import GL_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA, glBlendFunc, glEnable, GL_BLEND


class LightSource:
    def __init__(self, x, y, radius, color=(255, 255, 200), intensity=0.5):
        """
        Initialize a light source.
        :param x: X-coordinate of the light source.
        :param y: Y-coordinate of the light source.
        :param radius: Radius of the light source.
        :param color: RGB color of the light source (default: warm yellow).
        :param intensity: Intensity of the light (0.0 to 1.0, default: 0.5).
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.intensity = intensity

    def draw(self):
        """
        Draw the light source using additive blending.
        """
        # Enable blending for lighting effects
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Additive blending for light effects

        # Create and draw the light source
        light = pyglet.shapes.Circle(
            self.x, self.y, self.radius, color=self.color
        )
        light.opacity = int(self.intensity * 255)  # Convert intensity to opacity (0-255)
        light.draw()

        # Reset blending to default
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


class DynamicLightingManager:
    def __init__(self):
        """
        Manage multiple light sources for dynamic lighting.
        """
        self.light_sources = []

    def add_light(self, light_source):
        """
        Add a light source to the manager.
        :param light_source: An instance of LightSource.
        """
        self.light_sources.append(light_source)

    def remove_light(self, light_source):
        """
        Remove a light source from the manager.
        :param light_source: An instance of LightSource.
        """
        if light_source in self.light_sources:
            self.light_sources.remove(light_source)

    def draw_lights(self):
        """
        Draw all light sources managed by this manager.
        """
        for light in self.light_sources:
            light.draw()

    