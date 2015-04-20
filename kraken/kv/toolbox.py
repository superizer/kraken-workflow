from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.graphics import Line, Rectangle, Color, Triangle, Ellipse
from kivy.uix.spinner import Spinner
from kivy.uix.bubble import Bubble,BubbleButton
from kivy.uix.button import Button

from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from .widgets import DraggableWidget #, Component
from kraken.json_parser.read_json import CVFunctionParser
from kraken.configuration import settings

import math
import uuid
import copy

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
        
        if self.parent.tool_parameter.text == 'Select Parameter':
            return
                   
        h = 60
        w = 150
        ix = x - w/2
        iy = y - h/2
        fx = x + w/2
        fy = y + h/2
        
        widget = self.create_widget(ix,iy,fx,fy)
        (ix,iy) = widget.to_local(ix,iy,relative=True)
        (fx,fy) = widget.to_local(fx,fy,relative=True)
        widget.canvas.add(Color(0, 0.5, 0.5, 1))
        widget.canvas.add(Rectangle(pos=(ix, iy), size=(w,h)))
        widget.name = self.parent.tool_function.text
        widget.pars = copy.deepcopy(self.parent.tool_function.map_pars[self.parent.tool_parameter.text])
        #widget.pars = self.parent.tool_parameter.text
        widget.id = str(uuid.uuid1())
        
        l = Label(text=widget.name)
        widget.add_widget(l)
        
        if len(ds.children) == 0:
            widget.level = 0
        
        ds.add_widget(widget)
    
    def redraw(self, ds, x, y, name, wid, par, in_cv, out_cv,level):
                   
        h = 60
        w = 150
        ix = x - w/2
        iy = y - h/2
        fx = x + w/2
        fy = y + h/2
        
        widget = self.create_widget(ix,iy,fx,fy)
        (ix,iy) = widget.to_local(ix,iy,relative=True)
        (fx,fy) = widget.to_local(fx,fy,relative=True)
        widget.canvas.add(Color(0, 0.5, 0.5, 1))
        widget.canvas.add(Rectangle(pos=(ix, iy), size=(w,h)))
        widget.name = name
        widget.pars = par
        widget.id = wid
        widget.in_cv = in_cv
        widget.out_cv = out_cv
        widget.level = level
        
        l = Label(text=widget.name)
        widget.add_widget(l)
    
        ds.add_widget(widget)
    
    def create_widget(self,ix,iy,fx,fy):
        pos = (min(ix, fx), min(iy, fy)) 
        size = (abs(fx-ix), abs(fy-iy))
        return DraggableWidget(pos = pos, size = size)
    
class ToolLine(ToolButton):
    def create_figure(self,ix,iy,fx,fy):
        return Line(points=[ix, iy, fx, fy], width=1)
    
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

    def __init__(self,  **kwargs):
        self.read_obj = CVFunctionParser(settings['kraken_path'] + '/cvlibrary')
        super(ToolSelectLibrary, self).__init__(**kwargs)
    
    def show_selected_value(self, text):
        print('select library', self.text)
        
    def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        self.is_open = False
        #self.show_selected_value(self.text)
        #print('list values',self.values)
        self.set_select_function(self.text)
        
        
    def set_select_function(self,library_name):
        self.parent.tool_function.text='Select Function'
        self.parent.tool_parameter.text='Select Parameter'
        self.read_obj.get_from_json(library_name)
        list_funcs =self.read_obj.get_list_funs()
        self.parent.tool_function.values=set(list_funcs)
        
        
class ToolSelectFunction(Spinner):
    
    def __init__(self,  **kwargs):
        self.map_pars = {}
        self.bubble = None
        self.bubb_layout = None
        self.button = None
        self.func_des = None
        super(ToolSelectFunction, self).__init__(**kwargs)
    
    def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        self.is_open = False
        #print('select function',self.text)
        self.func_des = '[color=#ffff00][i][b]' + self.parent.tool_library.read_obj.get_func_des(self.text)+ '[/i][/b][/color]'
        self.set_select_parameter(self.text)
        
        if self.bubble is None:
            
            self.bubble = Bubble(size_hint=(.3, .2))
            self.bubb_layout = AnchorLayout(anchor_x='right', anchor_y='top')
            
            def remove_bubble(instance):
                self.bubb_layout.remove_widget(self.bubble)
                self.parent.parent.remove_widget(self.bubb_layout)
                self.bubble = None
                self.bubb_layout= None
                
            self.button = BubbleButton(text=self.func_des, halign = 'left', valign='middle', text_size = (300,300), background_color = (0, 0.5, 0.5, 1),markup=True)
            self.button.bind(on_press=remove_bubble)
            self.bubble.add_widget(self.button)
            self.bubble.arrow_pos = 'top_mid'
            self.bubb_layout.add_widget(self.bubble)
            self.parent.parent.parent.add_widget(self.bubb_layout)
        
        else:
            self.button.text = self.func_des
        
    def set_select_parameter(self,function):
        self.parent.tool_parameter.text='Select Parameter'
        self.map_pars = self.parent.tool_library.read_obj.get_pars_type(function)
        
        #print('map_pars',map_pars)
        self.parent.tool_parameter.values=self.map_pars.keys()
            
        
class ToolSelectParameter(Spinner):
    pass
    '''def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        self.is_open = False
        self.get_parameter_layout(self.text)
    
    def get_parameter_layout(self,function):
        print('pars', function)'''

    
     
        
    
