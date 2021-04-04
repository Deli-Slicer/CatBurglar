
import arcade

from CatBurglar import Window
from CatBurglar.Window import SCALED_WIDTH_PX, SCALED_HEIGHT_PX, TITLE, GameView


def main():
    window = arcade.Window(SCALED_WIDTH_PX, SCALED_HEIGHT_PX, TITLE)
    view = GameView()
    window.show_view(view)
    view.setup()
    arcade.run()

if __name__ == "__main__":
    main()
