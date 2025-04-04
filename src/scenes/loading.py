from engineclass.loading_base import LoadingSceneBase
from engineclass.CollidableAsset import CollidableAssetClass as CollidableAsset
from engineclass.PixelPerfect import PixelPerfectAsset
from engineclass.WalkThroughAsset import NonCollidableAsset as WalkThroughAsset
from engineclass.DynamicLightingObject import LightSource


class LoadingLevel_GameStartArea(LoadingSceneBase):
    def __init__(self, game):
        super().__init__(game)

    def load_level_specific_assets(self):
        # Load level-specific collidable assets
        from utils.helpers import imagepath
        self.collidable_assets = [
            CollidableAsset(400, 200, 20, 20, image_path=f"{imagepath}/bush.png", show_collision_box=True),
            CollidableAsset(300, 300, 20, 20, image_path=f"{imagepath}/lantern-silver.gif", show_collision_box=True),
        ]
        print(f"Log: Collidable assets loaded: {self.collidable_assets}")

        # Load level-specific non-collidable assets
        self.non_collidable_assets = [
            
        ]
        print(f"Log: Non-collidable assets loaded: {self.non_collidable_assets}")
        self.light_sources = [
            LightSource(300, 300, 150, color=(255, 255, 200), intensity=0.5),
            LightSource(500, 400, 100, color=(255, 200, 150), intensity=0.7),
        ]
        print(f"Log: Light sources loaded: {self.light_sources}")

        self.sounds = [

        ]
        print(f"Log: Sound assets loaded: {self.sounds}")
        self.enemies = []
        print(f"Log: Enemies loaded: {self.enemies}")
    
    def update(self, dt):
        self.load_assets()


    def load_assets(self):
        # Load player assets
        self.load_player(100,300)

        # Load level-specific assets
        self.load_level_specific_assets()

        # Finish loading
        self.finish_loading()