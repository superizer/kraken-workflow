from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window

Builder.load_file('toolbox.kv')
Builder.load_file('drawingspace.kv')
Builder.load_file('generaloptions.kv')
Builder.load_file('statusbar.kv')
Builder.load_file('widgets.kv')

class Kraken(AnchorLayout):
    pass

class KrakenApp(App):
    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)
        return Kraken()

if __name__ == "__main__":
    KrakenApp().run()
