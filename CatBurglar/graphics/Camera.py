
import arcade

class Camera:
    def __init__(self, width, height, pixel_perfect=False):

        self.width = width
        self.height = height

        self.width_center = width // 2
        self.height_center = height // 2

        self.pixel_perfect = pixel_perfect

        self.x = 0
        self.y = 0

        self.zoom_width = width
        self.zoom_height = height
        self.max_zoom_width = width * .54
        self.max_zoom_height = height * .54

        self.mouse_x = 0
        self.mouse_y = 0

        self.zoom_left = 0
        self.zoom_right = width
        self.zoom_bottom = 0
        self.zoom_top = height

        self.camera_lag = 2
        self.scroll_step = 0.005
        self.scroll_min_step = 0.1
        self.scroll_curr_step = 0.2

        self.old_x = 0
        self.old_y = 0

    def reset_viewport(self):
        arcade.set_viewport(0, self.width, 0, self.height)

    def set_viewport(self):
        if self.pixel_perfect:
            self.left = int(self.zoom_left + int(self.x) - self.width_center)
            self.right = int(self.zoom_right + int(self.x) - self.width_center)
            self.bottom = int(self.zoom_bottom + int(self.y) - self.height_center)
            self.top = int(self.zoom_top + int(self.y) - self.height_center)
        else:
            self.left = self.zoom_left + self.x - self.width_center
            self.right = self.zoom_right + self.x - self.width_center
            self.bottom = self.zoom_bottom + self.y - self.height_center
            self.top = self.zoom_top + self.y - self.height_center

        arcade.set_viewport(self.left, self.right, self.bottom, self.top)

    def scroll_to(self, x, y):

        x_diff = self.x - x
        y_diff = self.y - y

        if abs(x_diff) > self.camera_lag:
            self.x = self.x - self.scroll_curr_step * x_diff
        if abs(y_diff) > self.camera_lag:
            self.y = self.y - self.scroll_curr_step * y_diff

        self.old_x = x
        self.old_y = y

    def zoom(self, amount: float):
        self.zoom_width *= amount
        self.zoom_height *= amount

        if self.zoom_width < self.max_zoom_width:
            self.zoom_width = self.max_zoom_width
        if self.zoom_height < self.max_zoom_height:
            self.zoom_height = self.max_zoom_height

        self.set_zoom()

    def set_zoom(self):
        self.zoom_left   = self.width - self.zoom_width
        self.zoom_right  = self.zoom_width
        self.zoom_bottom = self.height - self.zoom_height
        self.zoom_top    = self.zoom_height

    def resize(self, width, height):

        self.zoom_width *= width / self.width
        self.zoom_height *= height / self.height

        self.width = width
        self.height = height

        self.width_center = width // 2
        self.height_center = height // 2

        self.set_zoom()
        self.set_viewport()
