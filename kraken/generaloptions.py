import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rotate, Color
from kivy.properties import NumericProperty, ListProperty
from toolbox import ToolLine
from numpy import ix_
import math
import uuid

from json_builder import KrakenJsonEncoder
import json

class GeneralOptions(BoxLayout):
    group_mode = True
    translation = ListProperty(None)

    def clear(self, instance):
        self.drawing_space.clear_widgets()

    def remove(self, instance):
        ds = self.drawing_space
        for child in ds.children:
            if child.selected:
                ds.remove_widget(child)
                self.status_bar.counter -= 1
                
    def remove_widget(self,widget):
        ds = self.drawing_space
        ds.remove_widget(widget)
        
    def remove_line(self,instance):
        ds = self.drawing_space
        for child in ds.children:
            if child.selected and child.line != None:
                ds.remove_widget(child.line)
                child.line = None
                child.to_widget.line = None
                child.to_widget.to_widget = None
                child.to_widget = None
                #self.status_bar.selected_counter -= 1
        self.unselect_all()
        
    def remove_line_between(self,instance):
        if self.status_bar.selected_counter is 2:
            ds = self.drawing_space
          
            for child in ds.children:
                if child.selected:
                    ds.remove_widget(child.line)
                    child.line = None
                    child.to_widget.line = None
                    child.to_widget.to_widget = None
                    child.to_widget = None
                    break
                    
            self.unselect_all()

    def line(self, instance):
        if self.status_bar.selected_counter is 2:
            
            ds = self.drawing_space
          
            list_child = []
            for child in ds.children:
                if child.selected:
                    list_child.append(child)
            
            if list_child[0].count == 1:
                line_widget = self.new_line(list_child[0], list_child[1])
                line_widget.widgetA = list_child[0]
                line_widget.widgetB = list_child[1]
            else:
                line_widget = self.new_line(list_child[1], list_child[0])
                line_widget.widgetA = list_child[1]
                line_widget.widgetB = list_child[0]
            
            line_widget.isLine = True
            line_widget.name = "Line"
            line_widget.id = str(uuid.uuid1())
           
            
            list_child[0].connect.append([list_child[1], line_widget])
            list_child[1].connect.append([list_child[0], line_widget])

            

            self.unselect_all()
            
    def new_line(self, widgetA, widgetB):
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
        
        '''mx = (ix+fx)/2
        my = (iy+fy)/2
        
        dx = fx - ix
        dy = fy - iy
        
        angle = None
        
        if dx != 0:
            #print('arctan : ' + str(math.atan(dy/dx)*57.2957795))
            angle = math.atan(dy/dx)*57.2957795
        else:
            #print('arctan : ' + str(90))
            angle = 90
            
        if angle < 0 :
            angle += 360
            
        print('angle : ' + str(angle))
        
        rot = Rotate()
        rot.angle = angle
        rot.axis = (0, 0, 1)
        rot.origin = (widgetB.x,widgetB.y)
        
        line_widget.canvas.add(rot)
        line_widget.canvas.add(tl.create_fig_arrow(ix,iy,fx,fy))'''
        line_widget.canvas.add(Color(1, 1, 0, 1))
        line_widget.canvas.add(tl.create_fig_arrow(ix,iy,fx,fy))
        line_widget.name ="Line"
        line_widget.id = str(uuid.uuid1())
        
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
                
    def to_json(self, instance):
        #print('generate JSON')
        
        
        
        cv = []
        for child in self.drawing_space.children:
            cv.append(child)
            
        
        
        workflow = dict(cv=cv)
        
        #jstr = json.dumps(workflow, cls=KrakenJsonEncoder)
        
        with open('/tmp/out.json', 'w') as f:
            json.dump(dict(workflow=workflow), f, cls=KrakenJsonEncoder)
        #print("json : ", jstr)
        
