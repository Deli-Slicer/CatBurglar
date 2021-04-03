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


class Player(Actor):

    def __init__(self, key_handler: KeyHandler, physics_engine: PhysicsEnginePlatformer = None):
        super().__init__(
           animations=GORILLA_TEXTURES)

        self.key_handler = key_handler

        # this should be changed ASAP, it's ugly and the platformer engine
        # doesn't do what we want anyway.
        self.physics_engine = physics_engine

        self.move_speed = 1
        self.jump_speed = 10

    def update(self):

        self.change_x *= .9

        if self.bottom > 0.1:
            #self.change_y -= .2
            pass
        else:
            self.change_y = 0
            self.bottom = 0
            self.jumping = False
        
        if self.key_handler.is_pressed("LEFT"):
            self.change_x -= self.move_speed
            self.current_animation_name = WALK_LEFT

        elif self.key_handler.is_pressed("RIGHT"):
            self.change_x += self.move_speed
            self.current_animation_name = WALK_RIGHT

        if self.key_handler.is_pressed("JUMP"):

            if self.physics_engine.can_jump():
                self.physics_engine.jump(10)

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

        super().update()

