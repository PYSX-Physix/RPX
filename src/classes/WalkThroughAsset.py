import pyglet

class NonCollidableAsset:
    def __init__(self, x, y, image_path, scale=1.0):
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load(image_path), x=x, y=y)
        self.sprite.scale = scale

    def draw(self):
        self.sprite.draw()