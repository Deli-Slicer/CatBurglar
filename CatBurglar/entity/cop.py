from arcade import load_texture

from CatBurglar.entity import NamedAnimationsSprite
from CatBurglar.input.KeyHandler import KeyHandler
from CatBurglar.util.asset_loading import ASSET_BASE_PATH


#!!! horrible kludge that should be replaced with proper asset loading helpers

COP_TEXTURES = {}

for anim_root in ['default', 'walk']:
    for direction in ['left', 'right']:
        template_str = f"{anim_root}_{direction}"
        itercieling = 4
        if anim_root == 'default':
            itercieling = 1

        if template_str not in COP_TEXTURES:
            COP_TEXTURES[template_str] = []

        for index in range(0, itercieling):
            COP_TEXTURES[template_str].append(
                load_texture(ASSET_BASE_PATH / f"cop/{template_str}_{index}.png")
            )

#!!! end horrible kludge


class Cop(NamedAnimationsSprite):
    """

    Temporary cop test asset for moving animations.

    """

    def __init__(self, key_handler: KeyHandler=None):
        #self.key_handler = key_handler
        super().__init__(animations=COP_TEXTURES, default_animation="walk_right")



