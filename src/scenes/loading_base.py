import pyglet
from scenes.game import GameScene

class LoadingSceneBase:
    def __init__(self, game):
        self.game = game
        self.player = None
        self.player_animations = {}
        self.collidable_assets = []
        self.non_collidable_assets = []
        self.light_sources = []
        self.enemies = []

    def update(self, dt):
        pass

    def load_player(self, direction):
        # Load player animations
        from utils.helpers import characterpath
        self.player_animations = {
            "idle_right": pyglet.image.load_animation(f"{characterpath}/dev_default/idle-right.gif"),
            "idle_left": pyglet.image.load_animation(f"{characterpath}/dev_default/idle-left.gif"),
            "left": pyglet.image.load_animation(f"{characterpath}/dev_default/move_left.gif"),
            "right": pyglet.image.load_animation(f"{characterpath}/dev_default/move_right.gif"),
            "up": pyglet.image.load_animation(f"{characterpath}/dev_default/move_up.gif"),
            "down": pyglet.image.load_animation(f"{characterpath}/dev_default/move_down.gif"),
        }
        self.player = pyglet.sprite.Sprite(self.player_animations[f"idle_{direction}"], x=100, y=100)
        print("Log: Player loaded.")

    def on_draw(self):
        # Clear the window
        self.game.window.clear()

        # Draw a loading screen
        loading_label = pyglet.text.Label(
            "Loading...",
            font_name="Arial",
            font_size=24,
            x=self.game.window.width // 2,
            y=self.game.window.height // 2,
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255),
        )
        loading_label.draw()

    def finish_loading(self):
        # Transition to the game scene
        game_scene = GameScene(
            self.game,
            player=self.player,
            player_animations=self.player_animations,
            collidable_assets=self.collidable_assets,
            non_collidable_assets=self.non_collidable_assets,
            light_sources=self.light_sources,
        )
        self.game.switch_scene(game_scene)