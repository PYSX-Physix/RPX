import pyglet
import numpy as np

class Player:
    def __init__(self, x, y, character_path, scale=1.0):
        # Load player animations
        self.animations = {
            "idle_right": pyglet.image.load_animation(f"{character_path}/dev_default/idle-right.gif"),
            "idle_left": pyglet.image.load_animation(f"{character_path}/dev_default/idle-left.gif"),
            "left": pyglet.image.load_animation(f"{character_path}/dev_default/move_left.gif"),
            "right": pyglet.image.load_animation(f"{character_path}/dev_default/move_right.gif"),
            "up": pyglet.image.load_animation(f"{character_path}/dev_default/move_up.gif"),
            "down": pyglet.image.load_animation(f"{character_path}/dev_default/move_down.gif"),
        }
        self.sprite = pyglet.sprite.Sprite(self.animations["idle_right"], x=x, y=y)
        self.sprite.scale = scale
        self.width = self.sprite.width
        self.height = self.sprite.height

        # Generate alpha mask for pixel-perfect collision
        self.alpha_mask = self._generate_alpha_mask(self.animations["idle_right"])

        # Movement state
        self.last_direction = "right"
        self.previous_x = x
        self.previous_y = y

    def _generate_alpha_mask(self, animation):
        """Generate an alpha mask for pixel-perfect collision."""
        if isinstance(animation, pyglet.image.Animation):
            frame_image = animation.frames[0].image
        else:
            frame_image = animation

        image_data = frame_image.get_image_data()
        raw_data = image_data.get_data("RGBA", image_data.width * 4)
        alpha_channel = raw_data[3::4]  # Extract every 4th byte (alpha channel)
        return np.frombuffer(alpha_channel, dtype=np.uint8).reshape(image_data.height, image_data.width)

    def move(self, dx, dy):
        """Move the player by dx and dy."""
        self.previous_x = self.sprite.x
        self.previous_y = self.sprite.y
        self.sprite.x += dx
        self.sprite.y += dy

    def set_animation(self, direction):
        """Set the player's animation based on direction."""
        if self.last_direction != direction:
            self.sprite.image = self.animations[direction]
            self.last_direction = direction

    def draw(self):
        """Draw the player sprite."""
        self.sprite.draw()