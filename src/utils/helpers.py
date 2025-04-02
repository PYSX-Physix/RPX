def load_image(file_path):
    from pyglet import image
    print(f"Loaded images at {file_path}")
    return image.load(file_path)

def load_sound(file_path, streaming: bool):
    from pyglet import media
    print(f"Loaded sound at {file_path} and streaming is set to {streaming}")
    return media.load(file_path, streaming)

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