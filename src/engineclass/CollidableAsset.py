import pyglet
import numpy as np

class CollidableAssetClass:
    def __init__(self, x, y, width, height, color=(200, 200, 200), image_path=None, scale: float = 1.0):
        if image_path:
            try:
                # Try to load the image as an animation (GIF)
                image = pyglet.image.load_animation(image_path)
                print(f"Log: Loaded animation: {image_path}")
            except Exception:
                # If it fails, load it as a static image
                image = pyglet.image.load(image_path)
                print(f"Log: Loaded static image: {image_path}")

            # Create a sprite for the image or animation
            self.sprite = pyglet.sprite.Sprite(image, x=x, y=y)
            self.sprite.scale = scale
            self.width = self.sprite.width
            self.height = self.sprite.height

            # Extract the alpha channel for pixel-perfect collision
            self.alpha_mask = self._generate_alpha_mask(image)
        else:
            print("Log: No sprite was given. Using default cube.")
            # Use a rectangle if no image is provided
            self.sprite = None
            self.shape = pyglet.shapes.Rectangle(x, y, width, height, color=color)
            self.width = width
            self.height = height
            self.alpha_mask = None  # No alpha mask for shapes

        self.x = x
        self.y = y

    def _generate_alpha_mask(self, image):
        """Generate an alpha mask for pixel-perfect collision."""
        if isinstance(image, pyglet.image.Animation):
            # Use the first frame of the animation
            frame_image = image.frames[0].image
        else:
            # Use the static image
            frame_image = image

        # Get the image data and extract the alpha channel
        image_data = frame_image.get_image_data()
        raw_data = image_data.get_data("RGBA", image_data.width * 4)
        alpha_channel = raw_data[3::4]  # Extract every 4th byte (alpha channel)
        return np.frombuffer(alpha_channel, dtype=np.uint8).reshape(image_data.height, image_data.width)

    def draw(self):
        if self.sprite:
            self.sprite.draw()
        else:
            self.shape.draw()

    def check_collision(self, sprite):
        # Get the width and height of the sprite's image (handles animations)
        if isinstance(sprite.image, pyglet.image.Animation):
            # Use the first frame of the animation to get dimensions
            sprite_width = sprite.image.frames[0].image.width
            sprite_height = sprite.image.frames[0].image.height
        else:
            sprite_width = sprite.image.width
            sprite_height = sprite.image.height

        return (
            sprite.x < self.x + self.width
            and sprite.x + sprite_width > self.x
            and sprite.y < self.y + self.height
            and sprite.y + sprite_height > self.y
        )