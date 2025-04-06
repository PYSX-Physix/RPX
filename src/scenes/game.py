import sys

import pyglet
from pyglet.math import Vec2
from utils.helpers import imagepath
# Engine Classes
from engineclass.player import Player
from engineclass.DynamicLightingObject import DynamicLightingManager


class GameScene:
    def __init__(self, game, player, collidable_assets, non_collidable_assets, light_sources, enemies, dynamic_lighting, background_image):
        self.game = game
        self.player = player
        self.collidable_assets = collidable_assets
        self.non_collidable_assets = non_collidable_assets
        self.light_sources = light_sources
        # Controller setup
        self.controller_manager = pyglet.input.ControllerManager()
        self.controller = None
        self.keys = {"left": False, "right": False, "up": False, "down": False}
        # Pause logic
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

        #Game background image
        self.background_image = background_image
        self.background_sprite = pyglet.sprite.Sprite(self.background_image, x=0, y=0)

        # Initialize pause menu buttons
        self.pause_menu_shapes = []
        self.pause_menu_labels = []
        self.pause_menu_buttons = []
    

        # Camera position
        self.camera_x = 0
        self.camera_y = 0

        self.initialize_pause_menu()
        self.initialize_controller()

    


    def initialize_controller(self):
        """Initialize the game controller."""
        input_controller = self.controller_manager.get_controllers()
        if input_controller:
            self.controller = input_controller[0]
            if self.controller.open == False:
                self.controller.open()
            elif self.controller.open == True:
                print("Log: Controller already open.")
                pass
            print(f"Log: Controller {self.controller.name} initialized.")

            # Set up controller events
            self.controller.on_dpad_motion = self.on_dpad_motion
            self.controller.on_button_press = self.on_button_press
            self.controller.on_button_release = self.on_button_release

        else:
            print("Log: No controller found.")

    

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
        # Draw the game background
        if self.background_sprite:
            self.background_sprite.draw()

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

            # Draw each light source with camera adjustment
            for light in self.light_sources:
                light.x -= self.camera_x
                light.y -= self.camera_y
                light.draw()
                light.x += self.camera_x
                light.y += self.camera_y

            # Reset blending to default
            pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    def on_draw(self):
        """Render the game scene."""
        self.game.window.clear()

        if self.paused:
            # Draw the pause menu background image
            self.pause_menu_background_sprite.draw()

            # Draw the pause menu buttons
            for button_shape, button_label in zip(self.pause_menu_shapes, self.pause_menu_labels):
                button_shape.draw()
                button_label.draw()
        else:
            # Adjust the background position based on the camera
            self.background_sprite.x = -self.camera_x
            self.background_sprite.y = -self.camera_y
            self.background_sprite.draw()

            # Adjust and draw the player
            self.player.sprite.x -= self.camera_x
            self.player.sprite.y -= self.camera_y
            self.player.draw()
            self.player.sprite.x += self.camera_x
            self.player.sprite.y += self.camera_y

            # Adjust and draw the enemies
            for enemy in self.enemies:
                enemy.sprite.x -= self.camera_x
                enemy.sprite.y -= self.camera_y
                enemy.draw()
                enemy.sprite.x += self.camera_x
                enemy.sprite.y += self.camera_y

            # Adjust and draw the collidable assets
            for asset in self.collidable_assets:
                asset.sprite.x -= self.camera_x
                asset.sprite.y -= self.camera_y
                asset.draw()
                asset.sprite.x += self.camera_x
                asset.sprite.y += self.camera_y

            # Adjust and draw the non-collidable assets
            for asset in self.non_collidable_assets:
                asset.sprite.x -= self.camera_x
                asset.sprite.y -= self.camera_y
                asset.draw()
                asset.sprite.x += self.camera_x
                asset.sprite.y += self.camera_y

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

            if symbol == pyglet.window.key.A:
                self.keys["left"] = True
                self.last_direction = "left"
            elif symbol == pyglet.window.key.D:
                self.keys["right"] = True
                self.last_direction = "right"
            elif symbol == pyglet.window.key.W:
                self.keys["up"] = True
            elif symbol == pyglet.window.key.S:
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

            if symbol == pyglet.window.key.A:
                self.keys["left"] = False
            elif symbol == pyglet.window.key.D:
                self.keys["right"] = False
            elif symbol == pyglet.window.key.W:
                self.keys["up"] = False
            elif symbol == pyglet.window.key.S:
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
    
    def on_joyaxis_motion(self, controller, stick, value: Vec2):
        """Handle joystick axis motion."""
        print(f"Log: Joystick axis {stick} moved with value {value}")

        if not self.paused:
            if stick == "leftstick":
                if value.x > -0.1:
                    self.keys["left"] = True
                    self.last_direction = "left"
                    print("Log: Left joystick moved left")
                elif value.x < 0.1:
                    self.keys["right"] = True
                    self.last_direction = "right"
                    print("Log: Left joystick moved right")
                elif value.y > -0.1:
                    self.keys["down"] = True
                    print("Log: Left joystick moved down")
                elif value.y < 0.1:
                    self.keys["up"] = True
                    print("Log: Left joystick moved up")
                elif value.x > -0.1:
                    self.keys["left"] = False
                    print("Log: Left joystick not moved left")
                elif value.x < 0.1:
                    self.keys["right"] = False
                    print("Log: Left joystick not moved right")
                elif value.y > -0.1:
                    self.keys["down"] = False
                    print("Log: Left joystick not moved down")
                elif value.y < 0.1:
                    self.keys["up"] = False
                    print("Log: Left joystick not moved up")
                elif value.x < 0.1:
                    self.keys["left"] = False
                    print("Log: Left joystick not moved left")
                elif value.x > -0.1:
                    self.keys["right"] = False
                    print("Log: Left joystick not moved right")
                elif value.y < 0.1:
                    self.keys["down"] = False
                    print("Log: Left joystick not moved down")
                elif value.y > -0.1:
                    self.keys["up"] = False
                    print("Log: Left joystick not moved up")
                



    def on_button_press(self, controller, button):
        """Handle button press events."""
        if button == "start":
            self.paused = not self.paused
        elif button == "a":
            print("Button A pressed")
        elif button == "b":
            print("Button B pressed")
        elif button == "x":
            print("Button X pressed")
        elif button == "y":
            print("Button Y pressed")

    def on_button_release(self, controller, button):
        """Handle button release events."""
        if button == "a":
            print("Button A released")
        elif button == "b":
            print("Button B released")
        elif button == "x":
            print("Button X released")
        elif button == "y":
            print("Button Y released")

    def on_dpad_motion(self, dpad, value: Vec2):
        """Handle D-pad motion events."""
        if not self.paused:
            if value.x < -0.1:
                self.keys["left"] = True
                self.last_direction = "left"
                print("Log: D-pad moved left")
            elif value.x > 0.1:
                self.keys["right"] = True
                self.last_direction = "right"
                print("Log: D-pad moved right")
            elif value.y < -0.1:
                self.keys["down"] = True
                print("Log: D-pad moved down")
            elif value.y > 0.1:
                self.keys["up"] = True
                print("Log: D-pad moved up")

            if value.x > -0.1:
                self.keys["left"] = False
                print("Log: D-pad not moved left")
            elif value.x < 0.1:
                self.keys["right"] = False
                print("Log: D-pad not moved right")
            elif value.y > -0.1:
                self.keys["down"] = False
                print("Log: D-pad not moved down")
            elif value.y < 0.1:
                self.keys["up"] = False
                print("Log: D-pad not moved up")


    def game_over(self):
        self.is_running = False
        # Transition to game over scene
        pass

    def update(self, dt):
        """Update the game logic and camera."""
        if self.is_running:
            self.update_game_logic()

        # Update the camera position
        self.update_camera()

    def update_game_logic(self):
        """Update the player's position and handle movement."""
        dx, dy = 0, 0
        if self.keys["left"]:
            dx -= 200 * 0.016
            print("Log: Moving left")
            if self.player.sprite.image != self.player_animations["left"]:
                self.player.sprite.image = self.player_animations["left"]
        if self.keys["right"]:
            dx += 200 * 0.016
            print("Log: Moving right")
            if self.player.sprite.image != self.player_animations["right"]:
                self.player.sprite.image = self.player_animations["right"]
        if self.keys["up"]:
            dy += 200 * 0.016
            print("Log: Moving up")
            if self.player.sprite.image != self.player_animations["up"]:
                self.player.sprite.image = self.player_animations["up"]
        if self.keys["down"]:
            dy -= 200 * 0.016
            print("Log: Moving down")
            if self.player.sprite.image != self.player_animations["down"]:
                self.player.sprite.image = self.player_animations["down"]

        # If no keys are pressed, set the idle animation
        if not (self.keys["left"] or self.keys["right"] or self.keys["up"] or self.keys["down"]):
            if self.last_direction == "left" and self.player.sprite.image != self.player_animations["idle_left"]:
                self.player.sprite.image = self.player_animations["idle_left"]
            elif self.last_direction == "right" and self.player.sprite.image != self.player_animations["idle_right"]:
                self.player.sprite.image = self.player_animations["idle_right"]

        # Update the player's position
        self.player.move(dx, dy, self.collidable_assets)

    def update_camera(self):
        """Update the camera position to follow the player."""
        screen_width = self.game.window.width
        screen_height = self.game.window.height

        # Center the camera on the player
        self.camera_x = self.player.sprite.x - screen_width // 2
        self.camera_y = self.player.sprite.y - screen_height // 2

        # Clamp the camera to the background boundaries
        self.camera_x = max(0, min(self.camera_x, self.background_image.width - screen_width))
        self.camera_y = max(0, min(self.camera_y, self.background_image.height - screen_height))

    def resume_game(self):
        self.paused = False  # Resume the game

    def restart_game(self):
        from scenes.loading import LoadingLevel_GameStartArea
        self.game.switch_scene(LoadingLevel_GameStartArea(self.game))  # Restart the game

    def quit_game(self):
        pyglet.app.exit()  # Quit the game