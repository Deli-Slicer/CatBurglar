
import arcade

WIDTH = 800
HEIGHT = 450

TITLE = "Cat Burglar"

RESIZABLE = False

class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=RESIZABLE)

    def setup(self):
        self.sprite_list = arcade.SpriteList()

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()