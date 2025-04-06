import pyglet
import numpy as np
from engineclass.player import Player


class CollidableAssetClass:
    def __init__(self, x, y, width, height, color=(200, 200, 200, 200), image_path=None, scale: float = 1.0,
                 collision_width=None, collision_height=None, collision_offset_x=0, collision_offset_y=0, show_collision_box=False):
        self.debug_collision_rect = None
        self.show_collision_box = show_collision_box

        if image_path != None:
            try:
                # Try to load the image as an animation (GIF)
                image = pyglet.image.load_animation(image_path)
                print(f"Log: Loaded animation: {image_path}")

                # Anchor each frame of the animation to the center
                for frame in image.frames:
                    frame.image.anchor_x = frame.image.width // 2
                    frame.image.anchor_y = frame.image.height // 2
            except Exception:
                # If it fails, load it as a static image
                image = pyglet.image.load(image_path)
                print(f"Log: Loaded static image: {image_path}")

                # Anchor the static image to the center
                image.anchor_x = image.width // 2
                image.anchor_y = image.height // 2

            # Create a sprite for the image or animation
            self.sprite = pyglet.sprite.Sprite(image, x=x, y=y)
            self.sprite.scale = scale
            self.width = int(self.sprite.width * scale)
            self.height = int(self.sprite.height * scale)
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

        # Collision box attributes (override default size if provided)
        self.collision_width = collision_width if collision_width is not None else self.width
        self.collision_height = collision_height if collision_height is not None else self.height
        self.collision_offset_x = collision_offset_x
        self.collision_offset_y = collision_offset_y

    def draw(self):
        """Draw the asset."""
        if self.sprite:
            self.sprite.draw()
            # Draw the collision box for debugging if enabled
            if self.show_collision_box:
                self.draw_debug_collision()
        else:
            self.shape.draw()

    def draw_debug_collision(self):
        """Draw the collision box for debugging."""
        if self.sprite:
            collision_x = self.sprite.x + self.collision_offset_x - self.collision_width // 2
            collision_y = self.sprite.y + self.collision_offset_y - self.collision_height // 2
            self.debug_collision_rect = pyglet.shapes.Rectangle(
                x=collision_x,
                y=collision_y,
                width=self.collision_width,
                height=self.collision_height,
                color=(255, 0, 0)  # Red color for the collision box
            )
            self.debug_collision_rect.draw()

    def check_collision(self, player):
        """
        Check for a bounding box collision with the player.
        :param player: The player object to check for collisions.
        :return: True if a collision is detected, False otherwise.
        """
        # Calculate the collision box for this asset
        asset_collision_x1 = self.sprite.x + self.collision_offset_x - self.collision_width // 2
        asset_collision_y1 = self.sprite.y + self.collision_offset_y - self.collision_height // 2
        asset_collision_x2 = asset_collision_x1 + self.collision_width
        asset_collision_y2 = asset_collision_y1 + self.collision_height

        # Calculate the collision box for the player
        player_collision_x1 = player.sprite.x
        player_collision_y1 = player.sprite.y
        player_collision_x2 = player_collision_x1 + player.width
        player_collision_y2 = player_collision_y1 + player.height

        # Check for overlap between the two collision boxes
        if (asset_collision_x1 < player_collision_x2 and
            asset_collision_x2 > player_collision_x1 and
            asset_collision_y1 < player_collision_y2 and
            asset_collision_y2 > player_collision_y1):
            return True

        return False


