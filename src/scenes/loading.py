import pyglet

class LoadingScene:
    def __init__(self, game):
        self.game = game
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
            "idle_right": pyglet.image.load_animation("src/assets/characters/dev_default/idle-right.gif"),
            "idle_left": pyglet.image.load_animation("src/assets/characters/dev_default/idle-left.gif"),
            "left": pyglet.image.load_animation("src/assets/characters/dev_default/move_left.gif"),
            "right": pyglet.image.load_animation("src/assets/characters/dev_default/move_right.gif"),
            "up": pyglet.image.load_animation("src/assets/characters/dev_default/move_up.gif"),
            "down": pyglet.image.load_animation("src/assets/characters/dev_default/move_down.gif"),
        }
        print(f"Log: Character: Animations: Loaded default animations {self.player_animations}")

        player_image = pyglet.image.load_animation("src/assets/characters/dev_default/dev_default.gif")
        self.player = pyglet.sprite.Sprite(self.player_animations["idle_right"], x=100, y=100)  # Initial position
        print(f"Log: GameScene: Player.Sprite: Loaded player with animation state {self.player_animations["idle_right"]} and spawned at {self.player.x} {self.player.y}")

        # Load enemies
        for i in range(5):  # Example: Load 5 enemies
            enemy = self.create_enemy(x=i * 100, y=200)
            self.enemies.append(enemy)

        # Load sounds
        print("There are no sounds loading because there are none.")  # Placeholder for sound loading

    def create_enemy(self, x, y):
        # Example enemy creation logic
        return pyglet.shapes.Rectangle(x, y, 50, 50, color=(255, 0, 0))

    def finish_loading(self):
        from scenes.game import GameScene
        # Pass the player, enemies, and sounds to the GameScene
        game_scene = GameScene(
            self.game, 
            player=self.player,
            player_animations=self.player_animations, 
            enemies=self.enemies, 
            sounds=self.sounds)
        self.game.switch_scene(game_scene)
        print(f"Log: Scene: Switched scene to {game_scene}")