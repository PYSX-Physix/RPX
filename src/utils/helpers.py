import os
import sys

basepath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(f"Base path: {basepath}")
imagepath = os.path.join(basepath, "assets", "images")
soundpath = os.path.join(basepath, "assets", "sounds")
characterpath = os.path.join(basepath, "assets", "characters")

def load_image(file_path):
    from pyglet import image
    print(f"Loaded images at {file_path}")
    return image.load(file_path)

def load_sound(file_path):
    from pyglet import media
    print(f"Loaded sound at {file_path}")
    return media.load(file_path, streaming=False)

def load_animation(frames, duration):
    from pyglet import sprite
    return sprite.Animation(frames, duration)

def save_game_state(state, file_path):
    import json
    with open(file_path, 'w') as f:
        json.dump(state, f)

def load_game_state(file_path):
    import json
    with open(file_path, 'r') as f:
        return json.load(f)