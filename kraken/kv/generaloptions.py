from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rotate, Color
from kivy.properties import NumericProperty, ListProperty, DictProperty
from .toolbox import ToolLine, ToolRectangle
from numpy import ix_

from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from ..configuration import settings
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import math
import uuid
import sys
import subprocess
import os

from kraken.json_builder import KrakenJsonEncoder
import json
from kivy.uix.stacklayout import StackLayout

class GeneralOptions(BoxLayout):
    group_mode = True
    translation = ListProperty(None)
    dic_name = DictProperty(None)

    def clear(self, instance):
        self.status_bar.selected_counter = 0
        self.drawing_space.clear_widgets()

    def remove(self, instance):
        ds = self.drawing_space
        for child in ds.children:
            if child.selected:
                if child.isLine is True:
                    child.widgetA.out_cv.remove(child.widgetB.id)
                    child.widgetB.in_cv.remove(child.widgetA.id)
                    child.widgetA.connect.remove([child.widgetB,child])
                    child.widgetB.connect.remove([child.widgetA,child])
                else:
                    for c in child.connect:
                        if child.id in c[0].in_cv:
                            c[0].in_cv.remove(child.id)
                        if child.id in c[0].out_cv:
                            c[0].out_cv.remove(child.id)
                        a = []
                        for k in c[0].connect:
                            if k[0] is child:
                                ds.remove_widget(k[1])
                            else:
                                a.append(k)
                        c[0].connect = a
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
            
            if list_child[0].count == 1:
                line_widget = self.new_line(list_child[0], list_child[1])
                line_widget.widgetA = list_child[0]
                line_widget.widgetB = list_child[1]
                list_child[0].out_cv.append(list_child[1].id)
                list_child[1].in_cv.append(list_child[0].id)
                
                if list_child[0].level != None:
                    list_child[1].level = list_child[0].level + 1
                elif list_child[1].level != None:
                    list_child[0].level = list_child[1].level - 1
            else:
                line_widget = self.new_line(list_child[1], list_child[0])
                line_widget.widgetA = list_child[1]
                line_widget.widgetB = list_child[0]
                list_child[1].out_cv.append(list_child[0].id)
                list_child[0].in_cv.append(list_child[1].id)
                
                if list_child[0].level != None:
                    list_child[1].level = list_child[0].level - 1
                elif list_child[1].level != None:
                    list_child[0].level = list_child[1].level + 1
            
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
        line_widget.isLine = True
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
                
    def run(self, instance):
        cv = []
        for child in self.drawing_space.children:
            cv.append(child)
            
        workflow = dict(cv=cv)
        
        jstr = json.dumps(dict(workflow=workflow), cls=KrakenJsonEncoder)
        
        p = subprocess.Popen([sys.executable, settings['kraken_path'] + '/kraken_backend/kraken.py'],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)
        out, _ = p.communicate(jstr.encode())
        #print(out.decode())
        
        #print('out',settings['kraken_path'] + '/kraken_backend/kraken.py')
        status = eval(out)
        
        popup = Popup(title='Running Status', size_hint=(None, None), size=(400, 180))
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=status['status']))
        b = Button(text='Close')
        b.bind(on_press=popup.dismiss)
        content.add_widget(b)
        popup.content = content
        popup.open()
                
    def to_json(self, instance):
        
        path = ''
        
        filechoser_layout = AnchorLayout()
        
        #filechoser = FileChooserIconView( size_hint = (0.75,0.85), path=settings['kraken_path'] +'/picture') #, multiselect = True)
        filechoser = FileChooserIconView( size_hint = (0.75,0.85), path='/home') #, multiselect = True)
        filechoser_list_layout = AnchorLayout(anchor_x='left', anchor_y='top')
        filechoser_list_layout.add_widget(filechoser)
        
        button_layout = AnchorLayout(anchor_x='left', anchor_y='bottom')
        
        box = BoxLayout(orientation='vertical', size_hint = (0.75,None), height = 96)
        
        bli =  BoxLayout(orientation='horizontal')
        ok_button = Button(text = 'Ok')
        cancel_button = Button(text = 'Cancel')
        
        
        bli2 =  BoxLayout(orientation='horizontal')
        ti = TextInput(size_hint = (1,None), height = 48)
        bli2.add_widget(Label(text = 'Enter File Name : '))
        bli2.add_widget(ti)
        
        bli.add_widget(ok_button)
        bli.add_widget(cancel_button)
        box.add_widget(bli2)
        box.add_widget(bli)
        button_layout.add_widget(box)
        
        image_layout = AnchorLayout(anchor_x='right', anchor_y='center')
        wimg = Image(source=settings['kraken_path'] +'/picture/girl.jpg',size_hint = (0.25,None),  size=(200,Window.size[1]))
        image_layout.add_widget(wimg)
        
        
        filechoser_layout.add_widget(filechoser_list_layout)
        filechoser_layout.add_widget(button_layout)
        filechoser_layout.add_widget(image_layout)
        
        popup_browser = Popup(title = 'Save File')
        popup_browser.add_widget(filechoser_layout)
        def save_path(instance):
            if ti.text != '':
                path = filechoser.path + '/' + ti.text
            else:
                path = filechoser.selection[0]
                
            # Save JSON
            
            cv = []
            for child in self.drawing_space.children:
                cv.append(child)
        
            workflow = dict(cv=cv)
        
            with open(path, 'w') as f:
                json.dump(dict(workflow=workflow), f, cls=KrakenJsonEncoder)    
            
            popup_browser.dismiss()
            
        def file_select(self, file): 
            if file:
                wimg.source = file[0]
        
        cancel_button.bind(on_press = popup_browser.dismiss)
        ok_button.bind(on_press = save_path)
        filechoser.bind(selection = file_select)
        
        popup_browser.open()
        
    def load_json(self, instance):
        
        path = ''
        
        filechoser_layout = AnchorLayout()
        
        #filechoser = FileChooserIconView( size_hint = (0.75,0.85), path=settings['kraken_path'] +'/picture') #, multiselect = True)
        filechoser = FileChooserIconView( size_hint = (0.75,0.85), path='/home') #, multiselect = True)
        filechoser_list_layout = AnchorLayout(anchor_x='left', anchor_y='top')
        filechoser_list_layout.add_widget(filechoser)
        
        button_layout = AnchorLayout(anchor_x='left', anchor_y='bottom')
        
        box = BoxLayout(orientation='vertical', size_hint = (0.75,None), height = 96)
        
        bli =  BoxLayout(orientation='horizontal')
        ok_button = Button(text = 'Ok')
        cancel_button = Button(text = 'Cancel')
        
        
        bli2 =  BoxLayout(orientation='horizontal')
        ti = TextInput(size_hint = (1,None), height = 48)
        bli2.add_widget(Label(text = 'Enter File Name : '))
        bli2.add_widget(ti)
        
        bli.add_widget(ok_button)
        bli.add_widget(cancel_button)
        box.add_widget(bli2)
        box.add_widget(bli)
        button_layout.add_widget(box)
        
        image_layout = AnchorLayout(anchor_x='right', anchor_y='center')
        wimg = Image(source=settings['kraken_path'] +'/picture/girl.jpg',size_hint = (0.25,None),  size=(200,Window.size[1]))
        image_layout.add_widget(wimg)
        
        
        filechoser_layout.add_widget(filechoser_list_layout)
        filechoser_layout.add_widget(button_layout)
        filechoser_layout.add_widget(image_layout)
        
        popup_browser = Popup(title = 'Open File')
        popup_browser.add_widget(filechoser_layout)
        def save_path(instance):
            if ti.text != '':
                path = filechoser.path + '/' + ti.text
            else:
                path = filechoser.selection[0]
           
            # Open From File
            ds = self.drawing_space
            self.clear(instance)
            
            with open(path) as json_file:
                json_data = json.load(json_file)
                funs = json_data['workflow']['cv']
                for fun in funs:
                    if fun['name'] != 'Line':
                        tr = ToolRectangle()
                        tr.redraw(ds,fun['pos']['x'],fun['pos']['y'],fun['name'],fun['id'],fun['pars'],fun['in_cv'],fun['out_cv'],fun['level'])
                for fun in funs:
                    if fun['name'] != 'Line':
                        for child in ds.children:
                            if child.id is fun['id']:
                                a = child
                                break
                        for b in fun['out_cv']:
                            for child in ds.children:
                                if child.id == b:
                                    line_widget = self.new_line(a, child)
                                    line_widget.widgetA = a
                                    line_widget.widgetB = child
                                    
                                    line_widget.isLine = True
                                    line_widget.name = "Line"
                                    line_widget.id = str(uuid.uuid1())
            
                                    a.connect.append([child, line_widget])
                                    child.connect.append([a, line_widget])
           
            popup_browser.dismiss()
            
        def file_select(self, file): 
            if file:
                wimg.source = file[0]
        
        cancel_button.bind(on_press = popup_browser.dismiss)
        ok_button.bind(on_press = save_path)
        filechoser.bind(selection = file_select)
        
        popup_browser.open()
        
    def show_time(self, instance):
        if instance.state == 'down':
            json_data = None
            if os.path.exists('/tmp/images/time.json'):
                f = open('/tmp/images/time.json')
                json_data = json.load(f)
                '''if self.id in json_data['time']:
                    self.parent.status_bar.process_time = json_data['time'][self.id]
                else:
                    self.parent.status_bar.process_time = 0'''
            else:
                return
            
            for child in self.drawing_space.children:
                #print('child.name = ' + child.name)
                t = ''
                if child.name is not 'Line':
                    #child.clear_widgets()
                    for c in child.children:
                        if type(c) is Label:
                            t = c.text
                            break
                    self.dic_name[child.id] = t
                    child.clear_widgets()    
                    l = Label(text= '[b]' + t + ' \n( ' + str(json_data['time'][child.id]) +' ms )[/b]',markup=True)
                    child.add_widget(l)
        elif instance.state == 'normal':
            if not os.path.exists('/tmp/images/time.json'):
                return
            for child in self.drawing_space.children:
                if child.name is not 'Line':
                    child.clear_widgets()    
                    l = Label(text=self.dic_name[child.id],markup=True)
                    child.add_widget(l)
            pass
            
            
        
        
        
