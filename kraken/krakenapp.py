from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kraken.kv import *
import os

from .configuration import settings

Builder.load_file(settings['kraken_path'] + '/kv/krakenlayout.kv')
Builder.load_file(settings['kraken_path'] + '/kv/toolbox.kv')
Builder.load_file(settings['kraken_path'] + '/kv/drawingspace.kv')
Builder.load_file(settings['kraken_path'] + '/kv/generaloptions.kv')
Builder.load_file(settings['kraken_path'] + '/kv/statusbar.kv')
Builder.load_file(settings['kraken_path'] + '/kv/widgets.kv')



class KrakenLayout(AnchorLayout):
    pass

class KrakenApp(App):
    def build(self):
        Window.size = (1400,800)
        #Window.clearcolor = (1, 1, 1, 1)
        kraken = KrakenLayout()
        lib = os.listdir(settings['kraken_path'] + '/cvlibrary')
        kraken.tool_box.tool_library.values = lib
        return kraken