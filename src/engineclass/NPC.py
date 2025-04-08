import pyglet
import random

class NPC:
    def __init__(self, name, image_path, x, y, scale: float = 1.0):
        self.load_animation(image_path, scale, x, y)
        self.name = name
        self.dialogue_chain = []
        self.dialogue_index = 0
        self.active = True
        

    def load_animation(self, image_path, scale: float = 1.0, x: int = 0, y: int = 0):
        if image_path != None:
            try:
                # Try to load the image as an animation (GIF)
                image = pyglet.image.load_animation(image_path)
                print(f"Log: Loaded animation for NPC: {image_path}")

                # Anchor each frame of the animation to the center
                for frame in image.frames:
                    frame.image.anchor_x = frame.image.width // 2
                    frame.image.anchor_y = frame.image.height // 2
            except Exception:
                # If it fails, load it as a static image
                image = pyglet.image.load(image_path)
                print(f"Log: Loaded static image for NPC: {image_path}")

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
            self.shape = pyglet.shapes.Rectangle(x, y, 50, 50, color=(255, 255, 255))  # Default white square
            self.alpha_mask = None  # No alpha mask for shapes


        self.x = x
        self.y = y

        
    def draw(self):
        if self.sprite:
            self.sprite.draw()

    def add_dialogue(self, prompt, options):
        formatted_options = []
        for opt in options:
            formatted_options.append({
                "text": opt["text"],
                "response": f"{self.name}: {opt['response']}",
                "condition": opt.get("condition", lambda: True)
            })
        self.dialogue_chain.append((f"{self.name}: {prompt}", formatted_options))

    def get_dialogue(self):
        if self.dialogue_index >= len(self.dialogue_chain):
            return None
        prompt, options = self.dialogue_chain[self.dialogue_index]
        available_options = [opt for opt in options if opt["condition"]()]
        return prompt, available_options

    def advance_dialogue(self):
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue_chain):
            self.active = False

