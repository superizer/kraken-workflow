from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

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
        
        self.input_pars = GridLayout(cols=2,size =(300,50))
        self.option_pars = GridLayout(cols=2,size =(300,50))
        
        
        #For Line
        self.widgetA = None
        self.widgetB = None
        
        super(DraggableWidget, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        
        if touch.is_double_tap and self.isLine == False:
            print("double tapp !!")
            
            
            self.input_pars.add_widget(Label(text = 'Parameter1'))
            self.input_pars.add_widget(TextInput())
            
            
            btn_save = Button(text='Save')
            btn_save.bind(on_press=self.save_param)
            btn_cancel = Button(text='Cancel')
            btn_cancel.bind(on_press=self.cancel_param)
            self.option_pars.add_widget(btn_save)
            self.option_pars.add_widget(btn_cancel)
            
        
            self.parent.tool_box.height = 250
            self.parent.tool_box.add_widget(self.input_pars)
            self.parent.tool_box.add_widget(self.option_pars)
        
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
            
    def save_param(self,instance):
        print('save parameter')
        self.input_pars.clear_widgets()
        self.option_pars.clear_widgets()
        self.parent.tool_box.remove_widget(self.input_pars)
        self.parent.tool_box.remove_widget(self.option_pars)
        self.parent.tool_box.height = 150
        
    def cancel_param(self,instance):
        print('cancel parameter')
        self.input_pars.clear_widgets()
        self.option_pars.clear_widgets()
        self.parent.tool_box.remove_widget(self.input_pars)
        self.parent.tool_box.remove_widget(self.option_pars)
        self.parent.tool_box.height = 150
