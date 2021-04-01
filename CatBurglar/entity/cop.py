from CatBurglar.entity import WALK_RIGHT, WALK_LEFT, REQUIRED_FOR_ACTORS, Actor, DRONE_REQUIRED_STATES
from CatBurglar.util import Timer
from CatBurglar.util.asset_loading import ASSET_BASE_PATH, preload_entity_texture_table, \
    preload_entity_texture_alt_skin_table

COP_PATH = ASSET_BASE_PATH / "cop"
DRONE_ASSET_PATH = ASSET_BASE_PATH / "drone"

COP_ALT_TABLE = preload_entity_texture_alt_skin_table(
    COP_PATH, REQUIRED_FOR_ACTORS
)


class BaseEnemy(Actor):
    """

    Baseclass for self-vanishing enemies that move left.

    """

    def __init__(
            self,
            default_animation=WALK_LEFT,
            animations=None,
            # base move velocity in px / sec
            base_move_velocity=-2.0
    ):
        super().__init__(
            animations=animations,
            alt_table=COP_ALT_TABLE,
            default_animation=default_animation,
        )

        # used to move left
        self.base_move_velocity=base_move_velocity

        #todo: if there's time, alter this so that it scales with a time constant?
        self.change_x = base_move_velocity

    def update(self, delta_time: float = 1/60):
        """
        Remove self from the game if we're past drawing

        :param delta_time: how big the delapsed delta is
        :return:
        """
        super().update()
        # get adjusted right-most boundary of the sprite
        rightmost_x = self.get_adjusted_hit_box()[1][0]
        if rightmost_x <= 0:
            self.remove_from_sprite_lists()


class BasicRunnerCop(BaseEnemy):
    """

    A basic ground-based enemy that goes left.

    """

    def __init__(
            self,
    ):
        super().__init__(
            default_animation=WALK_LEFT
        )

    def update(self, delta_time: float = 1 / 60):
        super().update()


DRONE_STATE_TABLE = preload_entity_texture_table(
    DRONE_ASSET_PATH,
    DRONE_REQUIRED_STATES
)

class Drone(BaseEnemy):

    def __init__(self, default_animation="fly_left"):
        super().__init__(
            animations=DRONE_STATE_TABLE,
            default_animation=default_animation
        )



