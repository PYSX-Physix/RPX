import pyglet

class SettingsScene:
    def __init__(self, game):
        self.game = game  # Reference to the Game instance

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

        # Back button
        self.back_button = pyglet.shapes.Rectangle(
            x=self.game.window.width // 2 - 100,
            y=200,
            width=200,
            height=40,
            color=(50, 50, 200),
        )
        self.back_label = pyglet.text.Label(
            "Back",
            font_name="Arial",
            font_size=16,
            x=self.game.window.width // 2,
            y=220,
            anchor_x="center",
            anchor_y="center",
        )

    def on_draw(self):
        # Clear the window and draw the settings menu
        self.game.window.clear()
        self.title_label.draw()
        self.lighting_button.draw()
        self.lighting_label.draw()
        self.back_button.draw()
        self.back_label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if the lighting button is clicked
        if (
            self.lighting_button.x <= x <= self.lighting_button.x + self.lighting_button.width
            and self.lighting_button.y <= y <= self.lighting_button.y + self.lighting_button.height
        ):
            self.toggle_lighting()

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
        self.game.save_settings()  # Save the updated setting

    def update(self, dt):
        # Placeholder for any updates in the settings scene
        pass