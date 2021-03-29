
import arcade

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 32

GRAVITY = 1

class Player(arcade.SpriteSolidColor):

    def __init__(self, key_handler):
        super().__init__(PLAYER_WIDTH, PLAYER_HEIGHT, arcade.color.AQUA)

        self.key_handler = key_handler

        self.move_speed = 1
        self.jump_speed = 4

    def update(self):

        self.change_x *= .9
        self.change_y *= .94
        
        if self.key_handler.is_pressed("LEFT"):
            self.change_x -= self.move_speed

        if self.key_handler.is_pressed("RIGHT"):
            self.change_x += self.move_speed

        if self.key_handler.is_pressed("UP"):
            self.change_y += self.jump_speed

        if self.key_handler.is_pressed("DOWN"):
            self.change_y -= self.move_speed

        super().update()

        if self.bottom < 0:
            self.bottom = 0
        # else:
        #     self.change_y -= GRAVITY