import os
import pyglet
from scenes.settings import SettingsScene  # Import the SettingsScene class
from utils.helpers import load_image, load_sound, imagepath, soundpath  # Import the load_image function


button_click_sound = os.path.join(soundpath, "button_click.wav")
button_click = load_sound(button_click_sound)

class MenuScene:
    def __init__(self, game):
        self.game = game  # Store the reference to the Game instance
        background_image_path = os.path.join(imagepath, "background.png")
        self.background_image = load_image(background_image_path)
        self.background_sprite = pyglet.sprite.Sprite(self.background_image, x=0, y=0)

        # Title label
        self.title_label = pyglet.text.Label(
            "RPX Game",
            font_name="Arial",
            font_size=24,
            x=self.game.window.width // 2,
            y=self.game.window.height - 100,
            anchor_x="center",
            anchor_y="center",
        )

        # Buttons
        self.buttons = [
            {"label": "Start Game", "x": self.game.window.width // 2, "y": 300, "action": self.start_game},
            {"label": "Options", "x": self.game.window.width // 2, "y": 250, "action": self.show_options},
            {"label": "Exit", "x": self.game.window.width // 2, "y": 200, "action": self.exit_game},
        ]
        self.button_shapes = []
        self.button_labels = []

        for button in self.buttons:
            # Create button background
            button_shape = pyglet.shapes.Rectangle(
                x=button["x"] - 100, y=button["y"] - 20, width=200, height=40, color=(50, 50, 200)
            )
            self.button_shapes.append(button_shape)

            # Create button label
            button_label = pyglet.text.Label(
                button["label"],
                font_name="Arial",
                font_size=16,
                x=button["x"],
                y=button["y"],
                anchor_x="center",
                anchor_y="center",
            )
            self.button_labels.append(button_label)

    def on_draw(self):
        # Clear the window and draw the title and buttons
        self.game.window.clear()
        self.background_sprite.draw()
        self.title_label.draw()

        for button_shape, button_label in zip(self.button_shapes, self.button_labels):
            button_shape.draw()
            button_label.draw()

    def update(self, dt):
        # Placeholder for any updates in the menu scene
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if a button was clicked
        for button_shape, button_data in zip(self.button_shapes, self.buttons):
            if (
                button_shape.x <= x <= button_shape.x + button_shape.width
                and button_shape.y <= y <= button_shape.y + button_shape.height
            ):
                button_click.play()
                button_data["action"]()  # Call the button's action

    # Button actions
    def start_game(self):
        from scenes.loading import LoadingScene
        self.game.switch_scene(LoadingScene(self.game))  # Switch to the loading scene
        # Add logic to switch to the game scene

    def show_options(self):
        self.game.switch_scene(self.game.settings_scene)  # Switch to the settings scene

    def exit_game(self):
        pyglet.app.exit()