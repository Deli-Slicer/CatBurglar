from typing import Type

import arcade
import pyglet.gl as gl
from arcade import SpriteList
from arcade.gui import UIManager, UILabel
from arcade.gui.ui_style import UIStyle

from CatBurglar.entity.physics import RunnerPhysicsEngine
from CatBurglar.entity.spawner import EnemySpawner
from CatBurglar.entity.terrain import AnimatedFloorTile, TILE_SIZE_PX, WIDTH_IN_TILES, HEIGHT_IN_TILES
from CatBurglar.input.KeyHandler import KeyHandler
from CatBurglar.graphics.Camera import Camera
from CatBurglar.entity.Player import Player, MoveState
from CatBurglar.entity.cop import BasicRunnerCop, Drone
from CatBurglar.util import StopwatchTimer


# size of display before viewport scaling
BASE_WIDTH_PX = WIDTH_IN_TILES * TILE_SIZE_PX
BASE_HEIGHT_PX = HEIGHT_IN_TILES * TILE_SIZE_PX

# upscaling for viewport size
ZOOM_FACTOR = 4
SCALED_WIDTH_PX = BASE_WIDTH_PX * ZOOM_FACTOR
SCALED_HEIGHT_PX = BASE_HEIGHT_PX * ZOOM_FACTOR


TITLE = "Cat Burglar"

RESIZABLE = False


def spawn_entities_from_map_layer(
        source_list: SpriteList,
        entity_type: Type,
        destination_list: SpriteList
):

        for reference in source_list:
            new_entity = entity_type()
            new_entity.set_position(reference.center_x, reference.center_y)
            destination_list.append(new_entity)

class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.physics_engine: RunnerPhysicsEngine = None
        self.wall_list: SpriteList = None
        self.key_handler: KeyHandler = None
        self.zoom_speed: float = None
        self.player: Player = None
        self.camera: None = None
        self.sprite_list: SpriteList = None
        self.enemy_list: SpriteList = None

        self.global_time_elapsed: StopwatchTimer = None
        self.enemy_spawner: EnemySpawner = None
        self.message_display_box = None
        self.ui_manager = UIManager()

    def setup(self):
        self.ui_manager.purge_ui_elements()

        self.message_display_box = UILabel(
            "Test text",
            center_x=BASE_WIDTH_PX / 2,
            center_y=3 * (BASE_HEIGHT_PX / 4)
        )

        self.message_display_box.set_style_attrs(
            font_name=["Courier", "Courier New", "Nimbus Mono"],
            font_size=8
        )
        self.ui_manager.add_ui_element(
            self.message_display_box
        )

        ground_level_y = TILE_SIZE_PX
        self.sprite_list = arcade.SpriteList()
        self.key_handler = KeyHandler()

#        self.camera = Camera(self.width, self.height, True)
#        self.zoom_speed = .95

        self.player = Player(self.key_handler)
        self.player.set_position(2 * TILE_SIZE_PX, ground_level_y)
        self.sprite_list.append(self.player)

        # the ground will animate to create the illusion of motion
        # instead of moving the floor tiles. the player never moves.
        self.wall_list = SpriteList(use_spatial_hash=True)

        # Enemies will be moving instead of the player and the ground
        self.enemy_list = SpriteList(use_spatial_hash=False)

        # game is 2 minutes long
        self.global_time_elapsed = StopwatchTimer(running=True, maximum=2 * 60.0)

        self.enemy_spawner = EnemySpawner(self.enemy_list, self.global_time_elapsed)

        # create the ground
        for x_position in range(0, WIDTH_IN_TILES * TILE_SIZE_PX, TILE_SIZE_PX):
            floor_tile = AnimatedFloorTile()
            floor_tile.set_position(TILE_SIZE_PX / 2 + x_position, TILE_SIZE_PX / 2)
            self.wall_list.append(floor_tile)

        self.physics_engine = RunnerPhysicsEngine(
            self.player,
            self.key_handler,
            self.enemy_list
        )

    def on_update(self, delta_time):
        self.global_time_elapsed.update(delta_time=delta_time)
        self.enemy_spawner.update(delta_time=delta_time)
        self.sprite_list.update()
        self.enemy_list.update()

        collisions = self.physics_engine.update()
        if collisions:
            print(f"Collided with the following entities: {collisions!r}")

        self.wall_list.update_animation()

        self.sprite_list.update_animation(delta_time=delta_time)
        self.enemy_list.update_animation(delta_time=delta_time)
        #if self.key_handler.is_pressed("ZOOM_IN"):
        #    self.camera.zoom(self.zoom_speed)
        #elif self.key_handler.is_pressed("ZOOM_OUT"):
        #    self.camera.zoom(1 / self.zoom_speed)

        #self.camera.scroll_to(self.player.center_x, self.player.center_y)

    def on_draw(self):
        arcade.start_render()

        # upscale by 4x
        arcade.set_viewport(0, SCALED_WIDTH_PX / 4, 0, SCALED_HEIGHT_PX / 4)

        # self.camera.set_viewport()
        self.sprite_list.draw(filter=gl.GL_NEAREST)
        self.enemy_list.draw(filter=gl.GL_NEAREST)
        self.wall_list.draw(filter=gl.GL_NEAREST)

    def on_key_press(self, key, modifiers):
        self.key_handler.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.key_handler.on_key_release(key, modifiers)

    def on_resize(self, width, height):
        pass
        #self.camera.resize(width, height)
