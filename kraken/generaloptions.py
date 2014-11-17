import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty
from toolbox import ToolLine

class GeneralOptions(BoxLayout):
    group_mode = True
    translation = ListProperty(None)

    def clear(self, instance):
        self.drawing_space.clear_widgets()

    def remove(self, instance):
        ds = self.drawing_space
        for child in ds.children:
            if child.touched:
                ds.remove_widget(child)
                self.status_bar.selected_counter -= 1

    def line(self, instance):
        if self.status_bar.selected_counter is 2:
            
            ds = self.drawing_space
            tl = ToolLine()
            
            list_child = []
            for child in ds.children:
                if child.selected:
                    list_child.append(child)
            
            list_child[0].to_widget=list_child[1]
            list_child[1].to_widget=list_child[0]
            
            ix = list_child[0].x + list_child[0].size[0]/2
            iy = list_child[0].y + list_child[0].size[1]/2
            fx = list_child[1].x + list_child[1].size[0]/2
            fy = list_child[1].y + list_child[1].size[1]/2

            tl.widgetize(ds, ix, iy, fx, fy)

            self.unselect_all()
    
    def unselect_all(self):
        for child in self.drawing_space.children:
            child.unselect()

    def on_translation(self,instance,value):
        for child in self.drawing_space.children:
            if child.selected:
                child.translate(*self.translation)
