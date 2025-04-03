import pyglet
import json
from classes.CollidableAsset import CollidableAssetClass as CollidableAsset
from classes.WalkThroughAsset import NonCollidableAsset
from classes.DynamicLightingObject import LightSource
from utils.helpers import characterpath, imagepath


class LoadingScene:
    def __init__(self, game):
        self.game = game
        self.settings = self.load_settings()
        self.loading_label = pyglet.text.Label(
            "Loading Assets...",
            font_name="Arial",
            font_size=24,
            x=self.game.window.width // 2,
            y=self.game.window.height // 2,
            anchor_x="center",
            anchor_y="center",
        )
        self.enemies = []
        self.sounds = {}
        self.player = None  # Placeholder for the player sprite

    def load_settings(self):
        settings_path = "settings.json"
        try:
            with open(settings_path, "r") as file:
                settings = json.load(file)
                print(f"Log: Settings loaded: {settings}")
                return settings
        except FileNotFoundError:
            print(f"Error: Game Settings: Settings.json not found. Using default settings.")
            return {"dynamic_lighting": False, "resolution": [1280, 720]}

    def on_draw(self):
        self.game.window.clear()
        self.loading_label.draw()

    def update(self, dt):
        # Simulate loading assets
        self.load_assets()
        self.finish_loading()

    def load_assets(self):
        # Load player GIF
        self.player_animations = {
            "idle_right": pyglet.image.load_animation(f"{characterpath}/dev_default/idle-right.gif"),
            "idle_left": pyglet.image.load_animation(f"{characterpath}/dev_default/idle-left.gif"),
            "left": pyglet.image.load_animation(f"{characterpath}/dev_default/move_left.gif"),
            "right": pyglet.image.load_animation(f"{characterpath}/dev_default/move_right.gif"),
            "up": pyglet.image.load_animation(f"{characterpath}/dev_default/move_up.gif"),
            "down": pyglet.image.load_animation(f"{characterpath}/dev_default/move_down.gif"),
        }
        print(f"Log: Character: Animations: Loaded default animations {self.player_animations}")

        player_image = pyglet.image.load_animation(f"{characterpath}/dev_default/dev_default.gif")
        self.player = pyglet.sprite.Sprite(self.player_animations["idle_right"], x=100, y=100)  # Initial position
        print(f"Log: GameScene: Player.Sprite: Loaded player with animation state {self.player_animations['idle_right']} and spawned at {self.player.x} {self.player.y}")

        # Load Light Sources
        self.light_sources = {
            LightSource(300, 300, 150, color= (255, 255, 200), intensity=0.5),  # Example light source
            LightSource(500, 400, 100, color=(255, 200, 150), intensity=0.7),  # Another light source
        }

        # Load enemies
        
        # Load collidable assets with images
        self.collidable_assets = [
            CollidableAsset(400, 200, 20, 20, 4.0, image_path=f"{imagepath}/bush.png"),
            CollidableAsset(300, 300, 20, 20, 1.0, image_path=f"{imagepath}/lantern-silver.gif"),
        ]
        print(f"Log: Collidable assets loaded: {len(self.collidable_assets)}")

        # Load non-collidable assets
        self.non_collidable_assets = [
            NonCollidableAsset(100, 100, f"{imagepath}/grass.png"),
        ]
        print(f"Log: Non-collidable assets loaded: {len(self.non_collidable_assets)}")

        # Load sounds
        print("There are no sounds loading because there are none.")  # Placeholder for sound loading

    def create_enemy(self, x, y):
        # Example enemy creation logic
        return pyglet.shapes.Rectangle(x, y, 50, 50, color=(255, 0, 0))

    def finish_loading(self):
        from scenes.game import GameScene
        # Pass assets to the GameScene
        game_scene = GameScene(
            self.game, 
            player=self.player,
            player_animations=self.player_animations, 
            enemies=self.enemies, 
            sounds=self.sounds,
            collidable_assets=self.collidable_assets,
            non_collidable_assets=self.non_collidable_assets,
            light_sources=self.light_sources,
            dynamic_lighting_enabled=self.settings.get("dynamic_lighting", False),  # Pass dynamic lighting setting
            )
        self.game.switch_scene(game_scene)
        print(f"Log: Scene: Switched scene to {game_scene}")