# core/root.py

from kivy.uix.widget import Widget
from kivy.clock import Clock
from widgets.control_button import ControlButton
from net.client import SocketClient
import copy


class ControllerRoot(Widget):

    def on_kv_post(self, base_widget):
        self.client = SocketClient()

        self.state = {
            "stick": {"x": 0.0, "y": 0.0}
        }

        self.last_sent_state = {}

        Clock.schedule_interval(self.update_and_send, 0)

    def set_target_ip(self, ip):
        self.client.set_address(ip, 5000)

    def update_and_send(self, dt):
        if not self.client.addr:
            return

        self.state["stick"]["x"] = self.ids.stick.x_axis
        self.state["stick"]["y"] = self.ids.stick.y_axis

        for w in self.children:
            if isinstance(w, ControlButton):
                self.state[w.name] = w.pressed

        if self.state != self.last_sent_state:
            self.client.send(self.state)
            self.last_sent_state = copy.deepcopy(self.state)

    def create_multibutton(self, names):
        label = "".join(names)
        btn = ControlButton(
            name=label,
            label=label,
            controls=names,
            size=(120, 120),
            pos=(300, 300)
        )
        self.add_widget(btn)
