
import arcade

from CatBurglar.input.KeyHandler import KeyHandler
from CatBurglar.graphics.Camera import Camera
from CatBurglar.entity.Player import Player

WIDTH = 800
HEIGHT = 450

MIN_WIDTH = 160
MIN_HEIGHT = 90

TITLE = "Cat Burglar"

RESIZABLE = True

class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=RESIZABLE)

        self.center_window()

        self.set_min_size(MIN_WIDTH, MIN_HEIGHT)

    def setup(self):
        self.sprite_list = arcade.SpriteList()
        self.key_handler = KeyHandler()

        self.camera = Camera(self.width, self.height, True)
        self.zoom_speed = .95

        self.player = Player(self.key_handler)
        self.player.set_position(128, 128)

        self.sprite_list.append(self.player)

                # Map name
        map_name = f":resources:tmx_maps/map2_level_1.tmx"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name="Platforms",
                                                      scaling=.5,
                                                      use_spatial_hash=True)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             1)

    def on_update(self, delta_time):
        self.sprite_list.update()
        self.physics_engine.update()

        if self.key_handler.is_pressed("ZOOM_IN"):
            self.camera.zoom(self.zoom_speed)
        elif self.key_handler.is_pressed("ZOOM_OUT"):
            self.camera.zoom(1 / self.zoom_speed)

        self.camera.scroll_to(self.player.center_x, self.player.center_y)

    def on_draw(self):
        arcade.start_render()

        self.camera.set_viewport()

        self.sprite_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):
        self.key_handler.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.key_handler.on_key_release(key, modifiers)

    def on_resize(self, width, height):
        self.camera.resize(width, height)