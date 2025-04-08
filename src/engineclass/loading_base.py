import pyglet
from scenes.game import GameScene
from engineclass.player import Player
from engineclass.CollidableAsset import CollidableAssetClass as CollidableAsset

class LoadingSceneBase:
    def __init__(self, game):
        self.game = game
        self.player = None
        self.player_animations = {}
        self.collidable_assets = []
        self.non_collidable_assets = []
        self.light_sources = []
        self.enemies = []
        self.npcs = []
        self.background_image = None
        self.sounds = []
        self.background_bounds = None

    def update(self, dt):
        if self.player and self.background_bounds:
            print (f"Log: Player position before clamping: x={self.player.sprite.x}, y={self.player.sprite.y}")
            self.player.clamp_to_bounds(self.background_bounds)
            print (f"Log: Player position after clamping: x={self.player.sprite.x}, y={self.player.sprite.y}")

    def load_player(self, start_x, start_y):
        # Load player animations
        from utils.helpers import characterpath
        self.player = Player(start_x, start_y, characterpath)
        print("Log: Player loaded.")

    def load_game_background(self):
        from utils.helpers import imagepath, load_image
        self.background_image = load_image(f"{imagepath}/RPX-GameMap.png")
        print("Log: Game background loaded.")
        self.background_bounds = {
            "x_min": 0,
            "x_max": self.background_image.width,
            "y_min": 0,
            "y_max": self.background_image.height,
        }

        print(f"Log: Background bounds set to: {self.background_bounds}")
        self.player.clamp_to_bounds(self.background_bounds)
        print(f"Log: Player position clamped to background bounds: x={self.player.sprite.x}, y={self.player.sprite.y}")
        self.collidable_assets = [
            CollidableAsset(500, 2500, 200, 200, image_path=None),
            CollidableAsset(600, 2500, 200, 200, image_path=None),
        ]

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
            collidable_assets=self.collidable_assets,
            non_collidable_assets=self.non_collidable_assets,
            light_sources=self.light_sources,
            dynamic_lighting=self.game.dynamic_lighting,
            enemies=self.enemies,
            background_image=self.background_image,  # Pass the background image to the game scene
            npcs=self.npcs,
        )
        self.game.switch_scene(game_scene)