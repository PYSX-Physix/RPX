import pyglet
import json
import os
from scenes.menu import MenuScene
from scenes.settings import SettingsScene

class Game:
    def __init__(self):
        self.window = pyglet.window.Window(width=800, height=600, caption="RPG Game")
        self.settings_file = "settings.json"
        self.dynamic_lighting = True  # Default setting

        # Load settings from file
        self.load_settings()

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

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def update(self, dt):
        self.current_scene.update(dt)

    def switch_scene(self, new_scene):
        self.current_scene = new_scene

    def save_settings(self):
        # Save settings to a JSON file
        settings = {"dynamic_lighting": self.dynamic_lighting}
        with open(self.settings_file, "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        # Load settings from a JSON file
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                self.dynamic_lighting = settings.get("dynamic_lighting", True)

if __name__ == "__main__":
    game = Game()
    pyglet.app.run()
    game.save_settings()  # Save settings when the game exits