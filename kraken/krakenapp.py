from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kraken.kv import *
import os,sys

import os
kraken_path = os.path.dirname(__file__)
Builder.load_file(kraken_path + '/kv/krakenapp.kv')
Builder.load_file(kraken_path + '/kv/toolbox.kv')
Builder.load_file(kraken_path + '/kv/drawingspace.kv')
Builder.load_file(kraken_path + '/kv/generaloptions.kv')
Builder.load_file(kraken_path + '/kv/statusbar.kv')
Builder.load_file(kraken_path + '/kv/widgets.kv')



class Kraken(AnchorLayout):
    pass

class KrakenApp(App):
    def build(self):
        Window.size = (1400,800)
        kraken = Kraken()
        lib = os.listdir('../cvlibrary')
        kraken.tool_box.tool_library.values = lib
        return kraken