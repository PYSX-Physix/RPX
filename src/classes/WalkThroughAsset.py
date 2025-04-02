import pyglet

class NonCollidableAsset:
    def __init__(self, x, y, image_path):
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load(image_path), x=x, y=y)

    def draw(self):
        self.sprite.draw()