import pyglet

class CollidableAssetClass:
    def __init__(self, x, y, width, height, color=(200, 200, 200), image_path=None, scale=1.0):
        if image_path:
            # Load the image as a sprite
            self.sprite = pyglet.sprite.Sprite(pyglet.image.load(image_path), x=x, y=y)
            self.width = self.sprite.width
            self.height = self.sprite.height
            self.sprite.scale = scale
        else:
            # Use a rectangle if no image is provided
            self.sprite = None
            self.shape = pyglet.shapes.Rectangle(x, y, width, height, color=color)
            self.width = width
            self.height = height

        self.x = x
        self.y = y

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