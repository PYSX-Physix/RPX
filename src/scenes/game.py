import pyglet

class GameScene:
    def __init__(self, game, player=None, player_animations=None, enemies=None, sounds=None):
        self.game = game
        self.player = player  # Player sprite
        self.player_animations = player_animations  # Animations for the player
        self.enemies = enemies if enemies else []  # Use preloaded enemies
        self.sounds = sounds if sounds else {}  # Use preloaded sounds
        self.score = 0
        self.is_running = True
        self.keys = {  # Track key states
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

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
            enemy.draw()  # Assuming enemies have a `draw` method

    def on_draw(self):
        self.game.window.clear()
        self.draw()

    def on_key_press(self, symbol, modifiers):
        # Update key states
        if symbol == pyglet.window.key.LEFT:
            self.keys["left"] = True
        elif symbol == pyglet.window.key.RIGHT:
            self.keys["right"] = True
        elif symbol == pyglet.window.key.UP:
            self.keys["up"] = True
        elif symbol == pyglet.window.key.DOWN:
            self.keys["down"] = True
        elif symbol == pyglet.window.key.SPACE:
            if "player_jump" in self.sounds:
                self.sounds["player_jump"].play()  # Play jump sound

    def on_key_release(self, symbol, modifiers):
        # Update key states
        if symbol == pyglet.window.key.LEFT:
            self.keys["left"] = False
        elif symbol == pyglet.window.key.RIGHT:
            self.keys["right"] = False
        elif symbol == pyglet.window.key.UP:
            self.keys["up"] = False
        elif symbol == pyglet.window.key.DOWN:
            self.keys["down"] = False

    def game_over(self):
        self.is_running = False
        # Transition to game over scene
        pass

    def update(self, dt):
        if self.is_running:
            self.update_game_logic()

    def update_game_logic(self):
        # Determine the direction of movement
        if self.keys["left"]:
            self.player.image = self.player_animations["left"]
            self.player.x -= 200 * 0.016  # Move left
        elif self.keys["right"]:
            self.player.image = self.player_animations["right"]
            self.player.x += 200 * 0.016  # Move right
        elif self.keys["up"]:
            self.player.image = self.player_animations["up"]
            self.player.y += 200 * 0.016  # Move up
        elif self.keys["down"]:
            self.player.image = self.player_animations["down"]
            self.player.y -= 200 * 0.016  # Move down
        else:
            # If no keys are pressed, set the animation to idle
            self.player.image = self.player_animations["idle"]

        # Example: Update enemy positions or states
        for enemy in self.enemies:
            enemy.x += 1  # Example movement logic