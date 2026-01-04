#widgets/control_button.py

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.app import App


class ControlButton(Widget):
    name = StringProperty("")
    label = StringProperty("")
    controls = ListProperty([])
    pressed = BooleanProperty(False)
    dragging = False

    def on_kv_post(self, base_widget):
        self.lbl = Label(text=self.label)
        self.add_widget(self.lbl)
        self.bind(pos=self.update_label, size=self.update_label)
        Clock.schedule_once(lambda dt: self.update_label(), 0)

    def update_label(self, *args):
        self.lbl.center = self.center

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False

        app = App.get_running_app()

        if app.edit_mode:
            self.dragging = True
            self.offset_x = self.x - touch.x
            self.offset_y = self.y - touch.y
        else:
            self.pressed = True

        return True

    def on_touch_move(self, touch):
        if self.dragging:
            self.pos = (
                touch.x + self.offset_x,
                touch.y + self.offset_y
            )

    def on_touch_up(self, touch):
        was_dragging = self.dragging
        self.dragging = False
        self.pressed = False

        if was_dragging:
            from kivy.app import App
            App.get_running_app().save_layout()

    def set_size_percent(self, value):
        try:
            value = max(1, min(100, int(value)))
            base = 120
            size = base * value / 50
            self.size = (size, size)
        except:
            pass
