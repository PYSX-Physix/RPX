import pyglet

class NonCollidableAsset:
    def __init__(self, x, y, image_path, scale: float = 1.0):
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
        else:
            print("Log: No image provided for NonCollidableAsset.")
            self.sprite = None

    def draw(self):
        if self.sprite:
            self.sprite.draw()