from CatBurglar.entity import WALK_RIGHT, WALK_LEFT, REQUIRED_FOR_ACTORS, Actor, DRONE_REQUIRED_STATES
from CatBurglar.util import Timer
from CatBurglar.util.asset_loading import ASSET_BASE_PATH, preload_entity_texture_table, \
    preload_entity_texture_alt_skin_table

COP_PATH = ASSET_BASE_PATH / "cop"
DRONE_ASSET_PATH = ASSET_BASE_PATH / "drone"

COP_ALT_TABLE = preload_entity_texture_alt_skin_table(
    COP_PATH, REQUIRED_FOR_ACTORS
)

class BaseCop(Actor):
    """

    Temporary cop test asset for moving animations.

    """

    def __init__(self, default_animation=WALK_RIGHT):
        super().__init__(
            animations=None,
            alt_table=COP_ALT_TABLE,
            default_animation=default_animation
        )


class FakePatrollingCop(BaseCop):
    """
    Not intended to be the basis of actual gameplay. Only encapsulate movement demo.

    There needs to be another baseclass added between NamedAnimationsSprite for
    mobile characters that has state change logic support for movement.
    """

    def __init__(
            self,
            default_animation=WALK_RIGHT,
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
                self.current_animation_name = WALK_RIGHT
            self.reverse_timer.remaining = self.delay_between_reversals


DRONE_STATE_TABLE = preload_entity_texture_table(
    DRONE_ASSET_PATH,
    DRONE_REQUIRED_STATES
)

class Drone(Actor):

    def __init__(self, default_animation="fly_hover"):
        super().__init__(
            animations=DRONE_STATE_TABLE,
            default_animation=default_animation
        )



