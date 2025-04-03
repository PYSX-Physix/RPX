import pyglet
from utils.helpers import imagepath, load_image
import os


class GameScene:
    def __init__(self, game, player=None, player_animations=None, enemies=None, sounds=None, collidable_assets=None, non_collidable_assets=None, light_sources=None, dynamic_lighting_enabled=False):
        self.game = game
        self.player = player  # Player sprite
        self.player_animations = player_animations  # Animations for the player
        self.enemies = enemies if enemies else []  # Use preloaded enemies
        self.sounds = sounds if sounds else {}  # Use preloaded sounds
        self.score = 0
        self.is_running = True
        self.paused = False  # Track whether the game is paused
        self.keys = {  # Track key states
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.collidable_assets = collidable_assets if collidable_assets else []  # List of collidable assets
        self.non_collidable_assets = non_collidable_assets if non_collidable_assets else []  # List of non-collidable assets
        self.light_sources =  light_sources if light_sources else []  # List of light sources
        self.last_direction = "right"  # Default direction
        self.dynamic_lighting_enabled = dynamic_lighting_enabled

        # Pause menu background image
        pause_background_path = os.path.join(imagepath, "background.png")
        self.pause_menu_background_image = load_image(pause_background_path)
        self.pause_menu_background_sprite = pyglet.sprite.Sprite(
            self.pause_menu_background_image, x=0, y=0
        )

        # Pause menu buttons
        self.pause_menu_buttons = [
            {"label": "Resume", "x": self.game.window.width // 2, "y": 300, "action": self.resume_game},
            {"label": "Restart", "x": self.game.window.width // 2, "y": 250, "action": self.restart_game},
            {"label": "Quit", "x": self.game.window.width // 2, "y": 200, "action": self.quit_game},
        ]
        self.pause_menu_shapes = []
        self.pause_menu_labels = []

        for button in self.pause_menu_buttons:
            # Create button background
            button_shape = pyglet.shapes.Rectangle(
                x=button["x"] - 100, y=button["y"] - 20, width=200, height=40, color=(50, 50, 200)
            )
            self.pause_menu_shapes.append(button_shape)

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
            self.pause_menu_labels.append(button_label)

    def setup(self):
        self.initialize_player()

    def initialize_player(self):
        # Load the player GIF and create a sprite
        player_image = pyglet.image.load_animation("src/assets/characters/dev_default/dev_default.gif")
        self.player = pyglet.sprite.Sprite(player_image, x=100, y=100)  # Initial position

    def draw(self):
        # Draw the player
        if self.player:
            self.player.draw()

        # Draw the enemies
        for enemy in self.enemies:
            enemy.draw()

        # Draw the collidable assets
        for asset in self.collidable_assets:
            asset.draw()

        # Draw the non-collidable assets
        for asset in self.non_collidable_assets:
            asset.draw()

    def on_draw(self):
        self.game.window.clear()
        if self.paused:
            # Draw the pause menu background image
            self.pause_menu_background_sprite.draw()

            # Draw the pause menu buttons
            for button_shape, button_label in zip(self.pause_menu_shapes, self.pause_menu_labels):
                button_shape.draw()
                button_label.draw()
        else:
            # Draw the game elements
            self.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            # Override the default quit behavior and toggle the pause menu
            self.paused = not self.paused  # Toggle the paused state
        elif not self.paused:  # Only handle movement keys if the game is not paused
            if symbol == pyglet.window.key.LEFT:
                self.keys["left"] = True
            elif symbol == pyglet.window.key.RIGHT:
                self.keys["right"] = True
            elif symbol == pyglet.window.key.UP:
                self.keys["up"] = True
            elif symbol == pyglet.window.key.DOWN:
                self.keys["down"] = True

    def on_key_release(self, symbol, modifiers):
        if not self.paused:  # Only handle key releases if the game is not paused
            if symbol == pyglet.window.key.LEFT:
                self.keys["left"] = False
            elif symbol == pyglet.window.key.RIGHT:
                self.keys["right"] = False
            elif symbol == pyglet.window.key.UP:
                self.keys["up"] = False
            elif symbol == pyglet.window.key.DOWN:
                self.keys["down"] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.paused:
            # Check if a pause menu button was clicked
            for button_shape, button_data in zip(self.pause_menu_shapes, self.pause_menu_buttons):
                if (
                    button_shape.x <= x <= button_shape.x + button_shape.width
                    and button_shape.y <= y <= button_shape.y + button_shape.height
                ):
                    button_data["action"]()  # Call the button's action

    def game_over(self):
        self.is_running = False
        # Transition to game over scene
        pass

    def update(self, dt):
        if self.is_running:
            self.update_game_logic()

    def update_game_logic(self):
        # Update light sources dynamically if enabled
        if self.dynamic_lighting_enabled:
            for light in self.light_sources:
                # Use the first frame of the animation to get the player's dimensions
                if isinstance(self.player.image, pyglet.image.Animation):
                    player_width = self.player.image.frames[0].image.width
                    player_height = self.player.image.frames[0].image.height
                else:
                    player_width = self.player.image.width
                    player_height = self.player.image.height

                # Update the light's position based on the player's position
                light.x = self.player.x + player_width // 2
                light.y = self.player.y + player_height // 2

        original_x = self.player.x
        original_y = self.player.y

        # Move left
        if self.keys["left"]:
            if self.player.image != self.player_animations["left"]:
                self.player.image = self.player_animations["left"]
                self.player._animation = self.player_animations["left"]  # Reset animation
            self.player.x -= 200 * 0.016  # Move left
            self.last_direction = "left"  # Update last direction

        # Move right
        if self.keys["right"]:
            if self.player.image != self.player_animations["right"]:
                self.player.image = self.player_animations["right"]
                self.player._animation = self.player_animations["right"]  # Reset animation
            self.player.x += 200 * 0.016  # Move right
            self.last_direction = "right"  # Update last direction

        # Move up
        if self.keys["up"]:
            if self.player.image != self.player_animations["up"]:
                self.player.image = self.player_animations["up"]
                self.player._animation = self.player_animations["up"]  # Reset animation
            self.player.y += 200 * 0.016  # Move up

        # Move down
        if self.keys["down"]:
            if self.player.image != self.player_animations["down"]:
                self.player.image = self.player_animations["down"]
                self.player._animation = self.player_animations["down"]  # Reset animation
            self.player.y -= 200 * 0.016  # Move down

        # If no keys are pressed, set the idle animation based on the last direction
        if not (self.keys["left"] or self.keys["right"] or self.keys["up"] or self.keys["down"]):
            if self.last_direction == "left" and self.player.image != self.player_animations["idle_left"]:
                self.player.image = self.player_animations["idle_left"]
                self.player._animation = self.player_animations["idle_left"]  # Reset animation
            elif self.last_direction == "right" and self.player.image != self.player_animations["idle_right"]:
                self.player.image = self.player_animations["idle_right"]
                self.player._animation = self.player_animations["idle_right"]  # Reset animation
            
        # Check for collisions
        for asset in self.collidable_assets:
            if asset.check_collision(self.player):
                # If collision occurs, reset the player's position
                self.player.x = original_x
                self.player.y = original_y
                print("Collision detected! Movement blocked.")
                break

    def resume_game(self):
        self.paused = False  # Resume the game

    def restart_game(self):
        from scenes.loading import LoadingScene
        self.game.switch_scene(LoadingScene(self.game))  # Restart the game

    def quit_game(self):
        pyglet.app.exit()  # Quit the game