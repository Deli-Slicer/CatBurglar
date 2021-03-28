
import arcade

from CatBurglar.input.KeyHandler import KeyHandler
from CatBurglar.entity.Player import Player

WIDTH = 800
HEIGHT = 450

TITLE = "Cat Burglar"

RESIZABLE = False

class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=RESIZABLE)

    def setup(self):
        self.sprite_list = arcade.SpriteList()
        self.key_handler = KeyHandler()

        self.player = Player(self.key_handler)
        self.player.set_position(32, 32)

        self.sprite_list.append(self.player)

    def on_update(self, delta_time):
        self.sprite_list.update()

    def on_draw(self):
        arcade.start_render()

        self.sprite_list.draw()

    def on_key_press(self, key, modifiers):
        self.key_handler.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.key_handler.on_key_release(key, modifiers)