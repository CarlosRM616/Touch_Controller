from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.app import App
import math


class Stick(Widget):
    x_axis = NumericProperty(0.0)
    y_axis = NumericProperty(0.0)

    dragging = False

    # porcentaje del radio que será zona muerta
    dead_zone_ratio = 0.15

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False

        app = App.get_running_app()

        if app.edit_mode:
            self.dragging = True
            self.offset_x = self.x - touch.x
            self.offset_y = self.y - touch.y

        return True

    def on_touch_move(self, touch):
        app = App.get_running_app()

        # mover el stick completo en modo edición
        if self.dragging and app.edit_mode:
            self.pos = (
                touch.x + self.offset_x,
                touch.y + self.offset_y
            )
            return True

        if app.edit_mode:
            return False

        # lógica normal del stick
        cx, cy = self.center
        dx = touch.x - cx
        dy = touch.y - cy

        distance = math.hypot(dx, dy)
        radius = self.width / 2
        dead_zone = radius * self.dead_zone_ratio
        max_radius = radius * 1.6

        # si el dedo se va demasiado lejos, ignorar
        if distance > max_radius:
            return True

        # zona muerta
        if distance < dead_zone:
            self.x_axis = 0
            self.y_axis = 0
            return True

        # limitar al radio máximo
        limited_distance = min(distance, radius)
        factor = limited_distance / distance

        nx = dx * factor
        ny = dy * factor

        self.x_axis = nx / radius
        self.y_axis = ny / radius

        return True

    def on_touch_up(self, touch):
        app = App.get_running_app()

        if self.dragging:
            self.dragging = False
            app.save_layout()
            return True

        if not app.edit_mode:
            Animation(
                x_axis=0,
                y_axis=0,
                d=0.12,
                t="out_quad"
            ).start(self)
            return True
