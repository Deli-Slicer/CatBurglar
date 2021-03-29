from arcade import load_texture

from CatBurglar.entity import NamedAnimationsSprite
from CatBurglar.entity.actor import WALK_RIGHT, WALK_LEFT
from CatBurglar.util import Timer
from CatBurglar.util.asset_loading import ASSET_BASE_PATH


#!!! horrible kludge that should be replaced with proper asset loading helpers

COP_TEXTURES = {}

for anim_root in ['still', 'walk']:
    for direction in ['left', 'right']:
        template_str = f"{anim_root}_{direction}"
        itercieling = 4
        if anim_root == 'still':
            itercieling = 1

        if template_str not in COP_TEXTURES:
            COP_TEXTURES[template_str] = []

        for index in range(0, itercieling):
            COP_TEXTURES[template_str].append(
                load_texture(ASSET_BASE_PATH / f"cop/{template_str}_{index}.png")
            )

#!!! end horrible kludge


class BaseCop(NamedAnimationsSprite):
    """

    Temporary cop test asset for moving animations.

    """

    def __init__(self, default_animation="walk_right"):
        super().__init__(animations=COP_TEXTURES, default_animation="walk_right")


class FakePatrollingCop(BaseCop):
    """
    Not intended to be the basis of actual gameplay. Only encapsulate movement demo.

    There needs to be another baseclass added between NamedAnimationsSprite for
    mobile characters that has state change logic support for movement.
    """

    def __init__(
            self,
            default_animation="walk_right",
            delay_between_reversals=3.0
    ):
        super().__init__(default_animation=default_animation)
        self.delay_between_reversals = delay_between_reversals
        self.reverse_timer = Timer(delay_between_reversals)

    def update(self, delta_time: float = 1 / 60):
        self.reverse_timer.update(delta_time)
        if self.reverse_timer.remaining <= delta_time:
            if self.current_animation_name == WALK_RIGHT:
                self.current_animation_name = WALK_LEFT
            else:
                self.current_animation_name == WALK_RIGHT
            self.reverse_timer.remaining = self.delay_between_reversals


