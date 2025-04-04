import pyglet
from utils.helpers import imagepath, load_image
from engineclass.player import Player
from engineclass.DynamicLightingObject import DynamicLightingManager


class GameScene:
    def __init__(self, game, player, collidable_assets, non_collidable_assets, light_sources, enemies, dynamic_lighting):
        self.game = game
        self.player = player
        self.collidable_assets = collidable_assets
        self.non_collidable_assets = non_collidable_assets
        self.light_sources = light_sources
        self.keys = {"left": False, "right": False, "up": False, "down": False}
        self.is_running = True  # Initialize the game as running
        self.paused = False  # Initialize the game as not paused

        # Dynamic Lighting
        self.dynamic_lighting_enabled = dynamic_lighting  # Use the passed dynamic lighting setting
        self.lighting_manager = DynamicLightingManager()
        self.last_direction = "right"  # Track the last direction for idle animation
        self.player_animations = player.animations if isinstance(player, Player) else {}
        self.enemies = enemies

        # Load the pause menu background image
        pause_background_image = pyglet.image.load(f"{imagepath}/background.png")
        self.pause_menu_background_sprite = pyglet.sprite.Sprite(pause_background_image, x=0, y=0)

        # Initialize pause menu buttons
        self.pause_menu_shapes = []
        self.pause_menu_labels = []
        self.pause_menu_buttons = []

        self.initialize_pause_menu()

    def initialize_pause_menu(self):
        """Initialize the pause menu buttons and their actions."""
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = self.game.window.height // 2 + 50

        # Define button actions
        button_actions = [
            {"label": "Resume", "action": self.resume_game},
            {"label": "Restart", "action": self.restart_game},
            {"label": "Quit", "action": self.quit_game},
        ]

        for i, button_data in enumerate(button_actions):
            # Create a button shape
            button_x = self.game.window.width // 2 - button_width // 2
            button_y = start_y - i * (button_height + button_spacing)
            button_shape = pyglet.shapes.Rectangle(
                button_x, button_y, button_width, button_height, color=(50, 50, 200)
            )
            self.pause_menu_shapes.append(button_shape)

            # Create a button label
            button_label = pyglet.text.Label(
                button_data["label"],
                font_name="Arial",
                font_size=18,
                x=button_x + button_width // 2,
                y=button_y + button_height // 2,
                anchor_x="center",
                anchor_y="center",
                color=(255, 255, 255, 255),
            )
            self.pause_menu_labels.append(button_label)

            # Store the button action
            self.pause_menu_buttons.append(button_data)

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

    def draw_dynamic_lighting(self):
        """Draw dynamic lighting effects."""
        if self.dynamic_lighting_enabled:
            # Enable additive blending for lighting effects
            pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
            pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)

            # Draw each light source
            for light in self.light_sources:
                light.draw()

            # Reset blending to default
            pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

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

            # Draw dynamic lighting if enabled
            if self.dynamic_lighting_enabled:
                self.draw_dynamic_lighting()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            # Override the default quit behavior and toggle the pause menu
            self.paused = not self.paused  # Toggle the paused state
        elif not self.paused:  # Only handle movement keys if the game is not paused
            if symbol == pyglet.window.key.LEFT:
                self.keys["left"] = True
                self.last_direction = "left"  # Update last direction
            elif symbol == pyglet.window.key.RIGHT:
                self.keys["right"] = True
                self.last_direction = "right"  # Update last direction
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
        original_x = self.player.sprite.x
        original_y = self.player.sprite.y

        # Move left
        if self.keys["left"]:
            if self.player.sprite.image != self.player_animations["left"]:
                self.player.sprite.image = self.player_animations["left"]  # Set the walking left animation
            self.player.sprite.x -= 200 * 0.016  # Move left
            self.last_direction = "left"  # Update last direction

        # Move right
        if self.keys["right"]:
            if self.player.sprite.image != self.player_animations["right"]:
                self.player.sprite.image = self.player_animations["right"]  # Set the walking right animation
            self.player.sprite.x += 200 * 0.016  # Move right
            self.last_direction = "right"  # Update last direction

        # Move up
        if self.keys["up"]:
            if self.player.sprite.image != self.player_animations["up"]:
                self.player.sprite.image = self.player_animations["up"]  # Set the walking up animation
            self.player.sprite.y += 200 * 0.016  # Move up

        # Move down
        if self.keys["down"]:
            if self.player.sprite.image != self.player_animations["down"]:
                self.player.sprite.image = self.player_animations["down"]  # Set the walking down animation
            self.player.sprite.y -= 200 * 0.016  # Move down

        # If no keys are pressed, set the idle animation based on the last direction
        if not (self.keys["left"] or self.keys["right"] or self.keys["up"] or self.keys["down"]):
            if self.last_direction == "left" and self.player.sprite.image != self.player_animations["idle_left"]:
                self.player.sprite.image = self.player_animations["idle_left"]  # Set idle left animation
            elif self.last_direction == "right" and self.player.sprite.image != self.player_animations["idle_right"]:
                self.player.sprite.image = self.player_animations["idle_right"]  # Set idle right animation
            elif self.last_direction == "up" and self.player.sprite.image != self.player_animations["idle_up"]:
                self.player.sprite.image = self.player_animations["idle_up"]  # Set idle up animation
            elif self.last_direction == "down" and self.player.sprite.image != self.player_animations["idle_down"]:
                self.player.sprite.image = self.player_animations["idle_down"]  # Set idle down animation

        # Check for collisions
        for asset in self.collidable_assets:
            if asset.check_collision(self.player):
                # If collision occurs, reset the player's position
                self.player.sprite.x = original_x
                self.player.sprite.y = original_y
                print(f"Collision detected! Movement blocked by an asset at {asset.x},{asset.y}.")
                break

    def resume_game(self):
        self.paused = False  # Resume the game

    def restart_game(self):
        from scenes.loading import LoadingLevel_GameStartArea
        self.game.switch_scene(LoadingLevel_GameStartArea(self.game))  # Restart the game

    def quit_game(self):
        pyglet.app.exit()  # Quit the game