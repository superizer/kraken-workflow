from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.graphics import Line, Rectangle, Color, Triangle, Ellipse
from kivy.uix.spinner import Spinner
from .widgets import DraggableWidget #, Component
from kraken.json_parser.read_json import CVFunctionParser
from kraken.configuration import settings

import math
import uuid

class ToolButton(ToggleButton):
    def on_touch_down(self, touch):
        ds = self.parent.drawing_space
        if self.state == 'down' and ds.collide_point(touch.x,touch.y):
            (x,y) = ds.to_widget(touch.x, touch.y)
            self.draw(ds, x, y)
            return True
        return super(ToolButton, self).on_touch_down(touch)

    def draw(self, ds, x, y):
        pass
    
class ToolRectangle(ToolButton):
    def draw(self, ds, x, y):
        h = 60
        w = 150
        ix = x - w/2
        iy = y - h/2
        fx = x + w/2
        fy = y + h/2
        
        widget = self.create_widget(ix,iy,fx,fy)
        (ix,iy) = widget.to_local(ix,iy,relative=True)
        (fx,fy) = widget.to_local(fx,fy,relative=True)
        widget.canvas.add(Color(1, 0, 0, 1))
        widget.canvas.add(Rectangle(pos=(ix, iy), size=(w,h)))
        widget.name = self.parent.tool_function.text
        widget.id = str(uuid.uuid1())
        
        l = Label(text=widget.name)
        widget.add_widget(l)
        ds.add_widget(widget)
    
    def create_widget(self,ix,iy,fx,fy):
        pos = (min(ix, fx), min(iy, fy)) 
        size = (abs(fx-ix), abs(fy-iy))
        return DraggableWidget(pos = pos, size = size)
    
class ToolLine(ToolButton):
    def create_figure(self,ix,iy,fx,fy):
        return Line(points=[ix, iy, fx, fy])
    
    def create_fig_arrow(self,ix,iy,fx,fy):
        
        
        mx = (ix+fx)/2
        my = (iy+fy)/2
        
        mmx = (mx + fx)/2
        mmy = (my + fy)/2
        
        d = 30
        return Ellipse(pos=(mmx - d / 2, mmy - d / 2), size=(d, d))
        
        '''dx = fx - ix
        dy = fy - iy
        
        
        if dx != 0:
            print('arctan : ' + str(math.atan(dy/dx)*57.2957795))
        else:
            print('arctan : ' + str(90))
        
        #if dx > dy:
        #    return Triangle(points = (mx,my,mmmx-50,mmmy+50,mmmx-50,mmmy-50))
        return Triangle(points = (mx,my,mx-50,my-50,mx-50,my+50))'''
        
    def create_widget(self,ix,iy,fx,fy):
        pos = (min(ix, fx), min(iy, fy)) 
        size = (abs(fx-ix), abs(fy-iy))
        return DraggableWidget(pos = pos, size = size)
    
class ToolSelectLibrary(Spinner):
    
    def show_selected_value(self, text):
        print('select library', self.text)
        
    def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        self.is_open = False
        #self.show_selected_value(self.text)
        #print('list values',self.values)
        self.set_select_function(self.text)
        
    def set_select_function(self,library_name):
        read_obj = CVFunctionParser(settings['kraken_path'] + '/cvlibrary')
        read_obj.get_from_json(library_name)
        list_funcs = read_obj.get_list_funs()
        self.parent.tool_function.values=list_funcs
        
        
class ToolSelectFunction(Spinner):
    
    def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        self.is_open = False
        #print('select function',self.text)
    
     
        
    
