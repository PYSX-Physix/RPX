from scenes.loading_base import LoadingSceneBase
from classes.CollidableAsset import CollidableAssetClass as CollidableAsset
from classes.WalkThroughAsset import NonCollidableAsset
from classes.DynamicLightingObject import LightSource


class LoadingLevel_GameStartArea(LoadingSceneBase):
    def __init__(self, game):
        super().__init__(game)

    def load_level_specific_assets(self):
        # Load level-specific collidable assets
        from utils.helpers import imagepath
        self.collidable_assets = [
            CollidableAsset(400, 200, 20, 20, image_path=f"{imagepath}/bush.png"),
            CollidableAsset(300, 300, 20, 20, image_path=f"{imagepath}/lantern-silver.gif"),
        ]
        print("Log: Level 1 collidable assets loaded.")

        # Load level-specific non-collidable assets
        self.non_collidable_assets = [
            
        ]
        if self.non_collidable_assets is None:
            print ("No walkthrough assets loaded skipping")
        print("Log: Level 1 non-collidable assets loaded.")
        self.light_sources = [
            LightSource(300, 300, 150, color=(255, 255, 200), intensity=0.5),
            LightSource(500, 400, 100, color=(255, 200, 150), intensity=0.7),
        ]
        print("Log: Level 1 light sources loaded.")

        print("No sounds loaded because none were specified")
    
    def update(self, dt):
        self.load_assets()


    def load_assets(self):
        # Load player assets
        self.load_player("right")

        # Load level-specific assets
        self.load_level_specific_assets()

        # Finish loading
        self.finish_loading()