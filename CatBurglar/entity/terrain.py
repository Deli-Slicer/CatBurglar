from CatBurglar.entity import NamedAnimationsSprite
from CatBurglar.util.asset_loading import (
    ASSET_BASE_PATH,
    preload_entity_texture_table
)

TILE_SIZE_PX = 16
TILE_PATH = ASSET_BASE_PATH / "tiles"

GROUND_BASE_PATH = TILE_PATH / "ground"

GROUND_ANIMATION_TABLE = preload_entity_texture_table(
    GROUND_BASE_PATH,
    ["ground_left"]
)


class AnimatedFloorTile(NamedAnimationsSprite):
    """
    Floor tile that interacts physically and provides illusion of movement.

    """
    def __init__(self):
        super(AnimatedFloorTile, self).__init__(
            animations=GROUND_ANIMATION_TABLE,
            default_animation="ground_left"
        )


