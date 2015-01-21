from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kraken.parameter import ParameterMenu

class DraggableWidget(RelativeLayout):
    def __init__(self,  **kwargs):
        
        self.selected = None
        self.touched = False
        
        self.isLine = False
        self.id = ""
        
        # For Component
        self.name = ""
        self.count = None
        #self.line = None
        #self.to_widget = None
        self.connect = [] # (to_widget : line)
        
        self.in_cv = []
        self.out_cv = []
        
        self.pars = {}
        #self.pars = ''
        
        #self.input_pars = GridLayout(cols=2,size =(300,50))
        #self.option_pars = GridLayout(cols=2,size =(300,50))
        
        
        #For Line
        self.widgetA = None
        self.widgetB = None
        
        super(DraggableWidget, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.touched is False:
                self.touched = True
                #if self.line is None:
                if self.parent.status_bar.selected_counter == 0:
                    self.count = 1
                else:
                    self.count = 2
                #print('self.count : ' + str(self.count))
                self.select()
            else:
                self.touched = False
                self.unselect()
                
            if touch.is_double_tap and self.isLine == False and len(self.pars) != 0:
                pm = ParameterMenu(self.pars,self.parent.tool_box)
                pm.create_pars_layout()
                #print('widget pars',self.pars)
                
            return True
        return super(DraggableWidget, self).on_touch_down(touch)

    def select(self):
        if not self.selected:
            self.parent.status_bar.selected_counter += 1;
            self.ix = self.center_x
            self.iy = self.center_y
            with self.canvas:
                self.selected = Line(rectangle=(0,0,self.width,self.height), dash_offset=2)

    def on_touch_move(self, touch):
        (x,y) = self.parent.to_parent(touch.x, touch.y)
        if self.selected and self.touched and self.parent.collide_point(x - self.width/2, y -self.height/2):
            go = self.parent.general_options
            go.translation=(touch.x-self.ix,touch.y-self.iy)
            return True
        return super(DraggableWidget, self).on_touch_move(touch)

    def translate(self, x, y):

        if self.connect is not None:
            go = self.parent.general_options

            for k in self.connect:
                widgetA = k[1].widgetA
                widgetB = k[1].widgetB
                
                go.remove_widget(k[1])
                
                for k in widgetA.connect:
                    if k[0] == widgetB:
                        k[1] = None
                        
                for k in widgetB.connect:
                    if k[0] == widgetA:
                        k[1] = None
                
                line_widget = go.new_line(widgetA, widgetB)
                line_widget.widgetA = widgetA
                line_widget.widgetB = widgetB
                
                for k in widgetA.connect:
                    if k[0] == widgetB:
                        k[1] = line_widget
                        
                for k in widgetB.connect:
                    if k[0] == widgetA:
                        k[1] = line_widget
            
        self.center_x = self.ix = self.ix + x
        self.center_y = self.iy = self.iy + y

    def unselect(self):
        if self.selected:
            self.parent.status_bar.selected_counter -= 1;
            #print('self.selected : ',str(self.selected) )
            self.canvas.remove(self.selected)
            self.selected = None  
