import pyglet
import numpy as np

class Player:
    def __init__(self, x, y, character_path, scale=1.0, show_hitbox=False):
        """
        Initialize the Player.
        :param x: The x-coordinate of the player.
        :param y: The y-coordinate of the player.
        :param character_path: Path to the player's animations.
        :param scale: Scaling factor for the player.
        :param show_hitbox: Whether to show the debug hitbox.
        """
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
        self.width = int(self.sprite.width)
        self.height = int(self.sprite.height)

        # Debug hitbox
        self.show_hitbox = show_hitbox
        self.hitbox = pyglet.shapes.Rectangle(
            x=self.sprite.x,
            y=self.sprite.y,
            width=self.width,
            height=self.height,
            color=(255, 0, 0),  # Red color for the hitbox
            batch=None  # No batch, drawn individually
        )

    def clamp_to_bounds(self, bounds):
        self.sprite.x = max(bounds["x_min"], min(self.sprite.x, bounds["x_max"] - self.width))
        self.sprite.y = max(bounds["y_min"], min(self.sprite.y, bounds["y_max"] - self.height))
        print(f"Log: Player position clamped to: x={self.sprite.x}, y={self.sprite.y}")

    def _generate_alpha_mask(self, image):
        """
        Generate an alpha mask for pixel-perfect collision detection.
        :param image: The image or animation to generate the mask from.
        :return: A NumPy array representing the alpha mask.
        """
        if isinstance(image, pyglet.image.Animation):
            # Use the first frame of the animation
            frame_image = image.frames[0].image
        else:
            frame_image = image

        image_data = frame_image.get_image_data()
        pitch = image_data.width * 4  # 4 bytes per pixel (RGBA)
        raw_data = image_data.get_data("RGBA", pitch)
        alpha_channel = raw_data[3::4]  # Extract every 4th byte (alpha channel)
        return np.frombuffer(alpha_channel, dtype=np.uint8).reshape(image_data.height, image_data.width)

    def _get_current_alpha_mask(self):
        """
        Get the alpha mask for the current frame of the player's animation.
        :return: A NumPy array representing the alpha mask.
        """
        if isinstance(self.sprite.image, pyglet.image.Animation):
            # Get the current frame of the animation
            current_frame = self.sprite.image.frames[self.sprite._frame_index].image
        else:
            # Use the static image
            current_frame = self.sprite.image

        return self._generate_alpha_mask(current_frame)

    def move(self, dx, dy, collidable_assets):
        """
        Move the player by dx and dy, resolving collisions with collidable assets.
        :param dx: Change in x position.
        :param dy: Change in y position.
        :param collidable_assets: List of CollidableAssetClass objects to check for collisions.
        """
        # Save the previous position
        self.previous_x = self.sprite.x
        self.previous_y = self.sprite.y

        # Attempt to move in the x direction
        self.sprite.x += dx
        for asset in collidable_assets:
            if asset.check_collision(self):  # Only check for collision status
                print("Collision in x direction detected.")
                # Resolve collision in the x direction
                self.sprite.x = self.previous_x
                break  # Stop checking further collisions in the x direction

        # Attempt to move in the y direction
        self.sprite.y += dy
        for asset in collidable_assets:
            if asset.check_collision(self):  # Only check for collision status
                print("Collision in y direction detected.")
                # Resolve collision in the y direction
                self.sprite.y = self.previous_y
                break  # Stop checking further collisions in the y direction

        # Update the hitbox position
        self.hitbox.x = self.sprite.x
        self.hitbox.y = self.sprite.y

    def set_animation(self, direction):
        if self.last_direction != direction:
            self.sprite.image = self.animations[direction]
            self.last_direction = direction

    def check_collision(self, collidable_asset):
        """
        Check for bounding box collision with a collidable asset.
        :param collidable_asset: An instance of CollidableAssetClass.
        :return: True if a collision is detected, False otherwise.
        """
        # Calculate the bounding box for the player
        player_x1 = self.sprite.x
        player_y1 = self.sprite.y
        player_x2 = player_x1 + self.width
        player_y2 = player_y1 + self.height

        # Calculate the bounding box for the collidable asset
        asset_x1 = collidable_asset.sprite.x
        asset_y1 = collidable_asset.sprite.y
        asset_x2 = asset_x1 + collidable_asset.width
        asset_y2 = asset_y1 + collidable_asset.height

        # Check for overlap between the two bounding boxes
        if (player_x1 < asset_x2 and
            player_x2 > asset_x1 and
            player_y1 < asset_y2 and
            player_y2 > asset_y1):
            print("Collision detected!")
            return True

        print("No collision detected.")
        return False

    def draw(self):
        """Draw the player sprite and optionally the debug hitbox."""
        self.sprite.draw()

        # Draw the debug hitbox if enabled
        if self.show_hitbox:
            self.hitbox.draw()