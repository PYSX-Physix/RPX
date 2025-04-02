import pyglet
import json
import os
from scenes.menu import MenuScene
from scenes.settings import SettingsScene

class Game:
    def __init__(self):
        self.window = pyglet.window.Window(width=1920, height=1080, caption="RPX Game")
        self.settings_file = "settings.json"
        self.dynamic_lighting = True  # Default setting
        self.resolution = (1920, 1080)  # Default resolution

        # Load settings from file
        self.load_settings()

        # Apply the loaded resolution
        self.window.set_size(*self.resolution)

        self.menu_scene = MenuScene(self)
        self.settings_scene = SettingsScene(self)
        self.current_scene = self.menu_scene

        @self.window.event
        def on_draw():
            self.current_scene.on_draw()

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            if hasattr(self.current_scene, "on_mouse_press"):
                self.current_scene.on_mouse_press(x, y, button, modifiers)

        @self.window.event
        def on_key_press(symbol, modifiers):
            if hasattr(self.current_scene, "on_key_press"):
                self.current_scene.on_key_press(symbol, modifiers)

        @self.window.event
        def on_key_release(symbol, modifiers):
            if hasattr(self.current_scene, "on_key_release"):
                self.current_scene.on_key_release(symbol, modifiers)

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def update(self, dt):
        self.current_scene.update(dt)

    def switch_scene(self, new_scene):
        self.current_scene = new_scene

    def save_settings(self):
        # Save settings to a JSON file
        settings = {
            "dynamic_lighting": self.dynamic_lighting,
            "resolution": self.resolution,
        }
        with open(self.settings_file, "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        # Load settings from a JSON file
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                self.dynamic_lighting = settings.get("dynamic_lighting", True)
                self.resolution = tuple(settings.get("resolution", (800, 600)))

if __name__ == "__main__":
    game = Game()
    pyglet.app.run()
    game.save_settings()  # Save settings when the game exits