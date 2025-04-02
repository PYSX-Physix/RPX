import pyglet
import os
import sys
from utils.helpers import load_sound, load_image, imagepath, soundpath


button_click_sound_path = os.path.join(soundpath, "button_click.wav")
button_click_Sound = load_sound(button_click_sound_path)

class SettingsScene:

    def __init__(self, game):
        self.game = game  # Reference to the Game instance
        background_image_path = os.path.join(imagepath, "background.png")
        self.background_image = load_image(background_image_path)
        self.background_sprite = pyglet.sprite.Sprite(self.background_image, x=0, y=0)

        # Title label
        self.title_label = pyglet.text.Label(
            "Settings",
            font_name="Arial",
            font_size=24,
            x=self.game.window.width // 2,
            y=self.game.window.height - 100,
            anchor_x="center",
            anchor_y="center",
        )

        # Dynamic lighting toggle button
        self.lighting_button = pyglet.shapes.Rectangle(
            x=self.game.window.width // 2 - 100,
            y=300,
            width=200,
            height=40,
            color=(50, 50, 200),
        )
        self.lighting_label = pyglet.text.Label(
            f"Dynamic Lighting: {'On' if self.game.dynamic_lighting else 'Off'}",
            font_name="Arial",
            font_size=16,
            x=self.game.window.width // 2,
            y=320,
            anchor_x="center",
            anchor_y="center",
        )

        # Resolution dropdown
        self.resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
        self.selected_resolution_index = self.resolutions.index(self.game.resolution)
        self.resolution_button = pyglet.shapes.Rectangle(
            x=self.game.window.width // 2 - 100,
            y=240,
            width=200,
            height=40,
            color=(50, 50, 200),
        )
        self.resolution_label = pyglet.text.Label(
            f"Resolution: {self.resolutions[self.selected_resolution_index][0]}x{self.resolutions[self.selected_resolution_index][1]}",
            font_name="Arial",
            font_size=16,
            x=self.game.window.width // 2,
            y=260,
            anchor_x="center",
            anchor_y="center",
        )

        # Back button
        self.back_button = pyglet.shapes.Rectangle(
            x=self.game.window.width // 2 - 100,
            y=120,
            width=200,
            height=40,
            color=(50, 50, 200),
        )
        self.back_label = pyglet.text.Label(
            "Back",
            font_name="Arial",
            font_size=16,
            x=self.game.window.width // 2,
            y=140,
            anchor_x="center",
            anchor_y="center",
        )

        self.restart_notice = pyglet.text.Label(
            "A restart is required to apply changes.",
            font_name="Arial",
            font_size=12,
            x=10,
            y=10,
            anchor_x="left",
            anchor_y="bottom",
            color=(255, 0, 0, 255),  # Red color for notice
        )

    def on_draw(self):
        # Clear the window and draw the settings menu
        self.game.window.clear()
        self.background_sprite.draw()
        self.title_label.draw()
        self.lighting_button.draw()
        self.lighting_label.draw()
        self.resolution_button.draw()
        self.resolution_label.draw()
        self.back_button.draw()
        self.back_label.draw()
        self.restart_notice.draw()  # Draw the restart notice

    def on_mouse_press(self, x, y, button, modifiers):
        # Load the button click sound
        
        button_click_Sound.play()
        
        # Check if the lighting button is clicked
        if (
            self.lighting_button.x <= x <= self.lighting_button.x + self.lighting_button.width
            and self.lighting_button.y <= y <= self.lighting_button.y + self.lighting_button.height
        ):
            self.toggle_lighting()

        # Check if the resolution button is clicked
        if (
            self.resolution_button.x <= x <= self.resolution_button.x + self.resolution_button.width
            and self.resolution_button.y <= y <= self.resolution_button.y + self.resolution_button.height
        ):
            self.cycle_resolution()

        # Check if the back button is clicked
        if (
            self.back_button.x <= x <= self.back_button.x + self.back_button.width
            and self.back_button.y <= y <= self.back_button.y + self.back_button.height
        ):
            self.game.switch_scene(self.game.menu_scene)  # Switch back to the menu scene

    def toggle_lighting(self):
        # Toggle the dynamic lighting setting
        self.game.dynamic_lighting = not self.game.dynamic_lighting
        self.lighting_label.text = f"Dynamic Lighting: {'On' if self.game.dynamic_lighting else 'Off'}"

    def cycle_resolution(self):
        # Cycle through the available resolutions
        self.selected_resolution_index = (self.selected_resolution_index + 1) % len(self.resolutions)
        selected_resolution = self.resolutions[self.selected_resolution_index]
        self.resolution_label.text = f"Resolution: {selected_resolution[0]}x{selected_resolution[1]}"
        self.game.resolution = selected_resolution

    def update(self, dt):
        # Placeholder for any updates in the settings scene
        pass