from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
#from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '800')


Builder.load_file('kv/kraken.kv')
Builder.load_file('kv/toolbox.kv')
Builder.load_file('kv/drawingspace.kv')
Builder.load_file('kv/generaloptions.kv')
Builder.load_file('kv/statusbar.kv')
Builder.load_file('kv/widgets.kv')

class Kraken(AnchorLayout):
    pass

class KrakenApp(App):
    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)
        return Kraken()

if __name__ == "__main__":
    KrakenApp().run()
