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

        # Create a radial gradient texture
        self.gradient_texture = self.create_gradient_texture()

    def create_gradient_texture(self):
        """
        Create a radial gradient texture for smooth lighting.
        """
        size = 256  # Texture size (higher = smoother gradient)
        gradient_image = pyglet.image.ImageData(size, size, 'RGBA', b'\x00' * size * size * 4)

        # Generate gradient data
        data = bytearray(size * size * 4)
        center = size // 2
        for y in range(size):
            for x in range(size):
                dx = x - center
                dy = y - center
                distance = (dx**2 + dy**2)**0.5 / center
                alpha = max(0, 1 - distance)  # Alpha decreases with distance
                index = (y * size + x) * 4
                data[index:index+4] = (255, 255, 255, int(alpha * 255))  # White with gradient alpha

        gradient_image.set_data('RGBA', size * 4, bytes(data))
        return gradient_image

    def draw(self):
        """
        Draw the light source using additive blending and a gradient texture.
        """
        # Enable blending for lighting effects
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Additive blending for light effects

        # Draw the gradient texture as a sprite
        sprite = pyglet.sprite.Sprite(self.gradient_texture, x=self.x - self.radius, y=self.y - self.radius)
        sprite.scale = self.radius / (self.gradient_texture.width // 2)  # Scale to match the radius
        sprite.color = self.color  # Apply the light color
        sprite.opacity = int(self.intensity * 255)  # Convert intensity to opacity (0-255)
        sprite.draw()

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

