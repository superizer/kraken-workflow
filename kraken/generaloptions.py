import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty
from toolbox import ToolLine
from numpy import ix_

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
                
    def remove_widget(self,widget):
        ds = self.drawing_space
        ds.remove_widget(widget)

    def line(self, instance):
        if self.status_bar.selected_counter is 2:
            
            ds = self.drawing_space
          
            list_child = []
            for child in ds.children:
                if child.selected:
                    list_child.append(child)
            
            list_child[0].to_widget=list_child[1]
            list_child[1].to_widget=list_child[0]
            
            line_widget = self.new_line(list_child[0], list_child[1])
            
            list_child[0].line = line_widget
            list_child[1].line = line_widget
            
            #ds.add_widget(line_widget)

            self.unselect_all()
            
    def new_line(self, widgetA, widgetB):
        
        # remove widgets before draw line
        ds = self.drawing_space
        ds.remove_widget(widgetA)
        ds.remove_widget(widgetB)
        
        ix = widgetA.x + widgetA.size[0]/2
        iy = widgetA.y + widgetA.size[1]/2
        fx = widgetB.x + widgetB.size[0]/2
        fy = widgetB.y + widgetB.size[1]/2

        tl = ToolLine()
        line_widget = tl.create_widget(ix,iy,fx,fy)
        (ix,iy) = line_widget.to_local(ix,iy,relative=True)
        (fx,fy) = line_widget.to_local(fx,fy,relative=True)
            
        line_widget.canvas.add(tl.create_figure(ix,iy,fx,fy))
        
        
        ds.add_widget(line_widget)
        ds.add_widget(widgetA)
        ds.add_widget(widgetB)
        
        return line_widget
        
    
    def unselect_all(self):
        for child in self.drawing_space.children:
            child.unselect()

    def on_translation(self,instance,value):
        for child in self.drawing_space.children:
            if child.selected:
                child.translate(*self.translation)
