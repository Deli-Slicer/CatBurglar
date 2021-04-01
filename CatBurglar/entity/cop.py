from CatBurglar.entity import WALK_RIGHT, WALK_LEFT, REQUIRED_FOR_ACTORS, Actor, DRONE_REQUIRED_STATES
from CatBurglar.util import Timer
from CatBurglar.util.asset_loading import ASSET_BASE_PATH, preload_entity_texture_table, \
    preload_entity_texture_alt_skin_table

COP_PATH = ASSET_BASE_PATH / "cop"
DRONE_ASSET_PATH = ASSET_BASE_PATH / "drone"

COP_ALT_TABLE = preload_entity_texture_alt_skin_table(
    COP_PATH, REQUIRED_FOR_ACTORS
)


class BaseRunnerEnemy(Actor):
    """

    Runs to the left, destroys self when it goes off screen.

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


class PatrollingCop(BaseRunnerEnemy):
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
        super().__init__(
            default_animation=default_animation,
        )
        self.delay_between_reversals = delay_between_reversals
        self.reverse_timer = Timer(delay_between_reversals)

    def update(self, delta_time: float = 1 / 60):
        super().update()

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

class Drone(BaseRunnerEnemy):

    def __init__(self, default_animation="fly_left"):
        super().__init__(
            animations=DRONE_STATE_TABLE,
            default_animation=default_animation
        )



