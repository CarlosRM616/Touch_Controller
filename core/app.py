#core/app.py

from kivy.app import App
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
import os
import json

from widgets.control_button import ControlButton
from widgets.stick import Stick
from core.root import ControllerRoot


class ControllerApp(App):
    edit_mode = BooleanProperty(False)
    selected_widget = ObjectProperty(None)

    def build(self):
        root = ControllerRoot()  # ✅ crear el root explícitamente

        # ===== PANEL DE CONEXIÓN =====
        self.conn_panel = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(360, 50)
        )

        def pos_conn(*a):
            self.conn_panel.pos = (400, root.height - 60)

        root.bind(size=pos_conn)
        pos_conn()

        self.ip_input = TextInput(
            hint_text="IP del PC",
            multiline=False,
            size_hint=(None, None),
            size=(220, 50)
        )

        connect_btn = Button(
            text="CONECTAR",
            size_hint=(None, None),
            size=(120, 50)
        )

        def connect(_):
            ip = self.ip_input.text.strip()
            if ip:
                root.set_target_ip(ip)

        connect_btn.bind(on_press=connect)

        self.conn_panel.add_widget(self.ip_input)
        self.conn_panel.add_widget(connect_btn)
        root.add_widget(self.conn_panel)

        # ======= BOTON EDIT =======
        self.edit_btn = Button(
            text="EDIT",
            size_hint=(None, None),
            size=(100, 50)
        )
        self.edit_btn.bind(on_press=self.toggle_edit)

        def pos_edit(*a):
            self.edit_btn.pos = (root.width - 120, root.height - 70)

        root.bind(size=pos_edit)
        pos_edit()
        root.add_widget(self.edit_btn)

        self.build_edit_panel(root)
        return root  # ✅ Kivy ahora sí asigna self.root

    def on_start(self):
        self.load_layout(self.root)

    def build_edit_panel(self, root):
        self.edit_panel = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(240, 300)
        )

        def pos_panel(*a):
            self.edit_panel.pos = (10, root.height - 310)
        root.bind(size=pos_panel)
        pos_panel()

        size_input = TextInput(hint_text="Tamaño 1-100", multiline=False)
        size_btn = Button(text="Aplicar tamaño")

        def apply_size(_):
            if self.selected_widget:
                self.selected_widget.set_size_percent(size_input.text)
                self.save_layout()

        size_btn.bind(on_press=apply_size)

        reset_btn = Button(text="Resetear layout")

        def reset_layout(_):
            # 1️⃣ borrar archivo de layout
            if os.path.exists("layout.json"):
                os.remove("layout.json")

            # 2️⃣ eliminar multibotones
            for w in list(self.root.children):
                if isinstance(w, ControlButton) and w.controls:
                    self.root.remove_widget(w)

            # 3️⃣ restaurar posiciones por defecto
            for w in self.root.children:
                if isinstance(w, Stick):
                    w.pos = (50, 50)
                    w.size = (200, 200)

                elif isinstance(w, ControlButton):
                    defaults = {
                        "A": (self.root.width - 170, 80),
                        "B": (self.root.width - 320, 80),
                        "C": (self.root.width - 170, 230),
                        "D": (self.root.width - 320, 230),
                        "COIN": (20, self.root.height - 80),
                        "START": (140, self.root.height - 80),
                    }
                    if w.name in defaults:
                        w.pos = defaults[w.name]
                        w.size = (120, 120)

            # 4️⃣ asegurar estado limpio
            self.edit_mode = False
            if self.edit_panel.parent:
                self.root.remove_widget(self.edit_panel)
            self.edit_btn.text = "EDIT"

        reset_btn.bind(on_press=reset_layout)

        delete_multi_btn = Button(text="Eliminar multibotones")

        def delete_multis(_):
            for w in list(root.children):
                if isinstance(w, ControlButton) and w.controls:
                    root.remove_widget(w)
            self.save_layout()

        delete_multi_btn.bind(on_press=delete_multis)

        multi_label = Label(text="Crear multibotón")
        toggle_layout = BoxLayout(size_hint_y=None, height=40)
        toggles = []

        for name in ["A", "B", "C", "D"]:
            t = ToggleButton(text=name)
            toggles.append(t)
            toggle_layout.add_widget(t)

        create_btn = Button(text="Crear")

        def create_multi(_):
            names = [t.text for t in toggles if t.state == "down"]
            if names:
                root.create_multibutton(names)
                for t in toggles:
                    t.state = "normal"
            self.save_layout()

        create_btn.bind(on_press=create_multi)

        self.edit_panel.add_widget(size_input)
        self.edit_panel.add_widget(size_btn)
        self.edit_panel.add_widget(reset_btn)
        self.edit_panel.add_widget(delete_multi_btn)
        self.edit_panel.add_widget(multi_label)
        self.edit_panel.add_widget(toggle_layout)
        self.edit_panel.add_widget(create_btn)

    def toggle_edit(self, instance):
        self.edit_mode = not self.edit_mode
        instance.text = "EDIT ON" if self.edit_mode else "EDIT"

        if self.edit_mode:
            self.root.add_widget(self.edit_panel)
        else:
            if self.edit_panel.parent:
                self.root.remove_widget(self.edit_panel)

    def save_layout(self):
        data = {}

        for w in self.root.children:
            if isinstance(w, Stick):
                data["Stick"] = {
                    "type": "stick",
                    "pos": list(w.pos),
                    "size": list(w.size)
                }

            elif isinstance(w, ControlButton):
                key = f"Button_{w.name}"
                data[key] = {
                    "type": "multi" if w.controls else "button",
                    "pos": list(w.pos),
                    "size": list(w.size),
                    "controls": w.controls
                }

        with open("layout.json", "w") as f:
            json.dump(data, f, indent=2)

    def load_layout(self, root):
        if not os.path.exists("layout.json"):
            return

        with open("layout.json", "r") as f:
            data = json.load(f)

        for key, info in data.items():
            if info["type"] == "multi":
                label = key.replace("Button_", "")
                btn = ControlButton(
                    name=label,
                    label=label,
                    controls=info["controls"],
                    size=info["size"],
                    pos=info["pos"]
                )
                root.add_widget(btn)

        for w in root.children:
            if isinstance(w, Stick) and "Stick" in data:
                w.pos = data["Stick"]["pos"]
                w.size = data["Stick"]["size"]

            elif isinstance(w, ControlButton):
                key = f"Button_{w.name}"
                if key in data:
                    w.pos = data[key]["pos"]
                    w.size = data[key]["size"]
