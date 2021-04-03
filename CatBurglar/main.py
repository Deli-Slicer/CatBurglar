
import arcade

from CatBurglar import Window
from CatBurglar.Window import WIDTH_PX, HEIGHT_PX, TITLE, GameView


def main():
    window = arcade.Window(WIDTH_PX, HEIGHT_PX, TITLE)
    view = GameView()
    window.show_view(view)
    view.setup()
    arcade.run()

if __name__ == "__main__":
    main()
