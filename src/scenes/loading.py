from engineclass.loading_base import LoadingSceneBase
from engineclass.CollidableAsset import CollidableAssetClass as CollidableAsset
from engineclass.PixelPerfect import PixelPerfectAsset
from engineclass.WalkThroughAsset import NonCollidableAsset as WalkThroughAsset
from engineclass.DynamicLightingObject import LightSource
from engineclass.NPC import NPC


class LoadingLevel_GameStartArea(LoadingSceneBase):
    def __init__(self, game):
        super().__init__(game)

    def load_level_specific_assets(self):
        # Load level-specific collidable assets
        from utils.helpers import imagepath, characterpath
        self.collidable_assets = [
            CollidableAsset(1600, 2500, 20, 20, image_path=f"{imagepath}/bush.png"),
            CollidableAsset(2000, 2500, 20, 20, image_path=f"{imagepath}/lantern-silver.gif"),
        ]
        print(f"Log: Collidable assets loaded: {self.collidable_assets}")

        # Load level-specific non-collidable assets
        self.non_collidable_assets = [
            
        ]
        print(f"Log: Non-collidable assets loaded: {self.non_collidable_assets}")
        self.light_sources = [
            LightSource(2000, 2500, 150, color=(255, 255, 200), intensity=0.5),
        ]
        print(f"Log: Light sources loaded: {self.light_sources}")

        self.sounds = [

        ]
        print(f"Log: Sound assets loaded: {self.sounds}")
        self.enemies = []
        print(f"Log: Enemies loaded: {self.enemies}")

        # Load level-specific NPCs
        self.npcs = [
            NPC("Shopkeeper", f"{characterpath}/dev_default/dev_default.gif", 2100, 2500),
        ]
        print(f"Log: NPCs loaded: {[npc.name for npc in self.npcs]}")


    def update(self, dt):
        self.load_assets()


    def load_assets(self):
        # Load player assets
        self.load_player(1800,2500)

        #Load the game background
        self.load_game_background()

        # Load level-specific assets
        self.load_level_specific_assets()

        # Finish loading
        self.finish_loading()