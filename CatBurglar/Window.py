from enum import Enum, auto
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
from CatBurglar.util import StopwatchTimer, CountdownTimer

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

class GameState(Enum):
    INTRO = auto()
    PLAYING = auto()
    LOST = auto()
    WON = auto()

INTRO_MESSAGE = """
They framed your cat for illegal stonks trades.
You're busting her out of jail.
Avoid the enemies for 2 minutes to escape!
Press SPACE to start!
"""

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

        self.message_display_box: UILabel = None
        self.message_timer = CountdownTimer()

        self.ui_manager = UIManager()
        self.game_state: GameState = GameState.INTRO

        # kludge to debounce the jump key
        self.game_over_debounce: bool = False

    def show_message(self, msg: str, duration: float = 2.0):

        # Extend timer instead of redrawing text
        if self.message_display_box.text == msg:
            self.message_timer.remaining = duration

            # It's ok to set the new message
        else:
            self.message_display_box.text = msg
            self.message_timer.remaining = duration


    def setup(self):
        self.ui_manager.purge_ui_elements()

        self.message_display_box = UILabel(
            INTRO_MESSAGE,
            center_x=BASE_WIDTH_PX / 2,
            center_y=3 * (BASE_HEIGHT_PX / 4),
            id="message_display_box"
        )

        # setting font doesn't appear to work
        self.message_display_box.set_style_attrs(
            font_name=["Courier", "Courier New", "Lucida Console"],
            font_size=7
        )

        self.ui_manager.add_ui_element(
            self.message_display_box
        )

        ground_level_y = TILE_SIZE_PX
        self.sprite_list = arcade.SpriteList()
        self.key_handler = KeyHandler()


        self.player = Player(self.key_handler)
        self.player.set_position(2 * TILE_SIZE_PX, ground_level_y * 2)
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

        if self.game_state == GameState.INTRO and self.key_handler.is_pressed("JUMP"):
            self.game_state = GameState.PLAYING
            self.show_message("Presss SPACE to jump")
            return

        elif self.game_state == GameState.PLAYING:

            self.global_time_elapsed.update(delta_time=delta_time)
            self.message_timer.update(delta_time=delta_time)

            # clear messages if need be
            if self.message_display_box.text and self.message_timer.remaining == 0:
                self.message_display_box.text = ""

            self.enemy_spawner.update(delta_time=delta_time)
            self.sprite_list.update()
            self.enemy_list.update()

            collisions = self.physics_engine.update()
            if collisions:
                self.game_state = GameState.LOST
                self.show_message("You have failed to escape!\nPress SPACE again to exit.")

            self.enemy_list.update_animation(delta_time=delta_time)
            self.sprite_list.update_animation(delta_time=delta_time)
            self.wall_list.update_animation(delta_time=delta_time)

            if self.global_time_elapsed.completion == 1.0:
                self.game_state = GameState.WON
                self.show_message("You have rescued your cat!\nPress SPACE again to exit.")

        elif self.game_state == GameState.LOST:
            if self.key_handler.is_pressed("JUMP"):
                if not self.game_over_debounce:
                    pass
                else:
                    self.window.close()
            else:
                self.game_over_debounce = True

        # end-of-competition rush, bad copy and paste code.
        elif self.game_state == GameState.LOST:
            if self.key_handler.is_pressed("JUMP"):
                if not self.game_over_debounce:
                    pass
                else:
                    self.window.close()
            else:
                self.game_over_debounce = True


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
