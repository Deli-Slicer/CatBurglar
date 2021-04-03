from enum import Enum, auto, unique

from arcade import PhysicsEngineSimple, PhysicsEnginePlatformer

from CatBurglar.entity import REQUIRED_FOR_ACTORS, Actor, WALK_LEFT, WALK_RIGHT, STILL_RIGHT, STILL_LEFT
from CatBurglar.input.KeyHandler import KeyHandler
from CatBurglar.util.asset_loading import ASSET_BASE_PATH, preload_entity_texture_table

GORILLA_SPRITE_PATH = ASSET_BASE_PATH / "gorilla"

GORILLA_TEXTURES = preload_entity_texture_table(
    GORILLA_SPRITE_PATH,
    REQUIRED_FOR_ACTORS
)

GRAVITY = 1


@unique
class MoveState(Enum):
   RUNNING = auto()
   JUMPING = auto()
   FALLING = auto()

class Player(Actor):

    def __init__(self, key_handler: KeyHandler, physics_engine: PhysicsEnginePlatformer = None):
        super().__init__(
           animations=GORILLA_TEXTURES,
            default_animation="catwalk_right"
        )

        self.key_handler = key_handler

        # this should be changed ASAP, it's ugly and the platformer engine
        # doesn't do what we want anyway.
        self.physics_engine = physics_engine

        self.move_speed = 1
        self.jump_speed = 10
        self._move_state = MoveState.RUNNING

    @property
    def move_state(self) -> MoveState:
        return self._move_state

    @move_state.setter
    def move_state(self, new_state):
        if new_state == MoveState.RUNNING:
            self.current_animation_name = "catwalk_right"
        else:
            self.current_animation_name = "catstill_right"

        self._move_state = new_state

    @property
    def jumping(self):
        return self.move_state == MoveState.JUMPING

    @property
    def running(self):
        return self.move_state == MoveState.RUNNING

    @property
    def falling(self):
        return self.move_state == MoveState.FALLING


    def update(self):

        """
        self.change_x *= .9

        if self.key_handler.is_pressed("LEFT"):
            self.change_x -= self.move_speed
            self.current_animation_name = WALK_LEFT

        elif self.key_handler.is_pressed("RIGHT"):
            self.change_x += self.move_speed
            self.current_animation_name = WALK_RIGHT

        """

        """
        elif self.key_handler.is_pressed("DOWN"):
            self.change_y -= self.move_speed

        # if we're below movement threshold but haven't updated
        # then set our still direction

        if self.moving:
            if abs(self.change_x) <= 0.1:
                if self.current_animation_name == WALK_LEFT:
                    self.current_animation_name = STILL_LEFT
                else:
                    self.current_animation_name = STILL_RIGHT
        """

        super().update()

