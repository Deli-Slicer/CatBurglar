from typing import Type

import arcade
import pyglet.gl as gl
from arcade import SpriteList

from CatBurglar.entity.terrain import AnimatedFloorTile
from CatBurglar.input.KeyHandler import KeyHandler
from CatBurglar.graphics.Camera import Camera
from CatBurglar.entity.Player import Player
from CatBurglar.entity.cop import BasicRunnerCop, Drone
from CatBurglar.util import Timer

WIDTH = 800
HEIGHT = 450

TILE_SIZE_PX = 16

MIN_WIDTH = 160
MIN_HEIGHT = 90

TITLE = "Cat Burglar"

RESIZABLE = True


def spawn_entities_from_map_layer(
        source_list: SpriteList,
        entity_type: Type,
        destination_list: SpriteList
):

        for reference in source_list:
            new_entity = entity_type()
            new_entity.set_position(reference.center_x, reference.center_y)
            destination_list.append(new_entity)

class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=RESIZABLE)

        self.center_window()

        self.set_min_size(MIN_WIDTH, MIN_HEIGHT)

        self.physics_engine: arcade.PhysicsEnginePlatformer = None
        self.wall_list: SpriteList = None
        self.key_handler: KeyHandler = None
        self.zoom_speed: float = None
        self.player: Player = None
        self.camera: None = None
        self.sprite_list: SpriteList = None
        self.enemy_list: SpriteList = None

    def setup(self):
        self.sprite_list = arcade.SpriteList()
        self.key_handler = KeyHandler()

        self.camera = Camera(self.width, self.height, True)
        self.zoom_speed = .95

        self.player = Player(self.key_handler)
        self.player.set_position(32, 32)

        # the ground will animate to create the illusion of motion
        # instead of moving the floor tiles. the player never moves.
        self.wall_list = SpriteList(use_spatial_hash=True)

        for x_position in range(-2 * TILE_SIZE_PX, 40 * TILE_SIZE_PX, TILE_SIZE_PX):
            floor_tile = AnimatedFloorTile()
            floor_tile.set_position(x_position, 16)
            self.wall_list.append(floor_tile)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             1)
        self.sprite_list.append(self.player)

        # these will always be moving
        self.enemy_list = SpriteList(use_spatial_hash=False)

        cop = BasicRunnerCop()
        cop.set_position(TILE_SIZE_PX * 35, 32)
        self.enemy_list.append(cop)
        self.sprite_list.append(cop)

        drone = Drone()
        drone.set_position(TILE_SIZE_PX * 10, TILE_SIZE_PX * 4)
        self.enemy_list.append(drone)

        self.sprite_list.append(drone)


    def on_update(self, delta_time):
        self.sprite_list.update()
        self.physics_engine.update()

        self.wall_list.update_animation()

        self.sprite_list.update_animation(delta_time=delta_time)

        if self.key_handler.is_pressed("ZOOM_IN"):
            self.camera.zoom(self.zoom_speed)
        elif self.key_handler.is_pressed("ZOOM_OUT"):
            self.camera.zoom(1 / self.zoom_speed)

        self.camera.scroll_to(self.player.center_x, self.player.center_y)

    def on_draw(self):
        arcade.start_render()

        self.camera.set_viewport()

        self.sprite_list.draw(filter=gl.GL_NEAREST)

        self.wall_list.draw(filter=gl.GL_NEAREST)

    def on_key_press(self, key, modifiers):
        self.key_handler.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.key_handler.on_key_release(key, modifiers)

    def on_resize(self, width, height):
        self.camera.resize(width, height)
