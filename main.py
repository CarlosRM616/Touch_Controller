#main.py

from kivy.app import App
from kivy.lang import Builder

# IMPORTANTE: registrar clases ANTES de cargar KV
from widgets.stick import Stick
from widgets.control_button import ControlButton
from core.root import ControllerRoot
from core.app import ControllerApp

Builder.load_file("controller.kv")

ControllerApp().run()

#192.168.5.102