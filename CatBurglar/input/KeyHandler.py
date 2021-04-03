
import arcade

from arcade.key import *

class KeyHandler:

    class Key:
        def __init__(self, key_codes):
            self.key_codes = list(key_codes)
            self.pressed = False
            self.clicked = False

    def __init__(self):

        self.key_codes_list = {}
        self.keys = {}

        self.add_key("JUMP", SPACE)

        self.add_key("UP", UP, W)
        self.add_key("DOWN", DOWN, S)
        self.add_key("LEFT", LEFT, A)
        self.add_key("RIGHT", RIGHT, D)

        self.add_key("ZOOM_OUT", MINUS)
        self.add_key("ZOOM_IN", EQUAL)
        self.add_key("FULLSCREEN", F10)
        self.add_key("ESC", ESCAPE)
        self.add_key("ENTER", ENTER)

    def on_key_press(self, key: int, modifiers: int):
        if self.key_codes_list.get(key):
            self.key_codes_list.get(key).pressed = True

    def on_key_release(self, key: int, modifiers: int):
        if self.key_codes_list.get(key):
            self.key_codes_list.get(key).pressed = False

    def is_pressed(self, key):
        return self.keys.get(key).pressed

    def add_key(self, key, *key_codes: int):
        if self.keys.get(key):
            for key_code in key_codes:
                self.keys[key].key_codes.append(key_code)
        else:
            self.keys[key] = self.Key(key_codes)

        for key_code in key_codes:
            self.key_codes_list[key_code] = self.keys[key]
