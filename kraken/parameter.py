'''
Created on Jan 15, 2015

@author: superizer
'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from .configuration import settings

import cv2

class InputForm(TextInput):
    
    def __init__(self, toolbox,  **kwargs):
        self.toolbox = toolbox
        super(InputForm, self).__init__(**kwargs)
        
    def on_double_tap(self):
        #print('hello tappp !!')
        ds = self.toolbox.drawing_space
        for child in ds.children:
            if child.selected:
                #print('select :',child.id)
                self.text = 'id=' + child.id
                
    def on_triple_tap(self):
        
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
        
        popup_browser = Popup(title = 'Select File')
        popup_browser.add_widget(filechoser_layout)
        def save_path(instance):
            if ti.text != '':
                self.text = filechoser.path + '/' + ti.text
            else:
                self.text = filechoser.selection[0]
            popup_browser.dismiss()
            
        def file_select(self, file): 
            if file:
                wimg.source = file[0]
        
        cancel_button.bind(on_press = popup_browser.dismiss)
        ok_button.bind(on_press = save_path)
        filechoser.bind(selection = file_select)
        
        popup_browser.open()

class ParameterMenu():
    def __init__(self, pars_dict,toolbox,widget):
        self.pars_dict = pars_dict
        self.toolbox = toolbox
        self.input_pars = GridLayout(cols=2,size =(300,50))
        self.option_pars = GridLayout(cols=2,size =(300,50))
        self.list_input_pars = []
        self.widget = widget
        
    def create_pars_layout(self):
        #self.input_pars.add_widget(Label(text = 'Parameter1'))
        #self.input_pars.add_widget(TextInput())
        
        self.input_pars = GridLayout(cols=2,size =(300,50*len(self.pars_dict)))
        
        for par in self.pars_dict:

            self.input_pars = GridLayout(cols=2,size =(300,50))
            self.input_pars.add_widget(Label(text = par['name']))

            ti = InputForm(text=str(par['value']),toolbox=self.toolbox)
            self.input_pars.add_widget(ti)
            
            self.list_input_pars.append(self.input_pars)
            #self.toolbox.add_widget(self.input_pars)
        
        for par in self.list_input_pars:
            self.toolbox.add_widget(par)
            
        def save_pars(instance):

            par_name = ''
            par_value = ''
            
            for par in self.list_input_pars:
                for child in par.children:
                    #if type(child) is TextInput:
                    if type(child) is InputForm:
                        par_value = child.text
                    elif type(child) is Label:
                        par_name = child.text
                        
                for parr in self.pars_dict:
                    if parr['name'] == par_name and par_value != '':
                        '''if parr['type'] == 'int':
                            if len(par_value) > 6 and (par_value[0:6] == "COLOR_" or par_value[0:3] == "cv2"):
                                if par_value[0:6] == "COLOR_":
                                    par_value = 'cv2.' + par_value
                                parr['value'] = eval(par_value)
                            else:
                                parr['value'] = int(par_value)
                        elif parr['type'] == 'double' or parr['type'] == 'float':
                            parr['value'] = float(par_value)
                        else:
                            #parr['value'] = par_value
                            try:
                                v = eval(par_value)
                            except:
                                v = par_value
                            print('type',type(v))
                            parr['value'] = v'''
                        parr['value'] = par_value
                    elif parr['name'] == par_name and par_value == '':
                        parr['value'] = ''
                
                self.toolbox.remove_widget(par)
            
            self.list_input_pars.clear()
            self.input_pars.clear_widgets()
            self.option_pars.clear_widgets()
            
            self.toolbox.remove_widget(self.option_pars)
            self.toolbox.height = 200
            
            if self.widget.selected_par:
                self.widget.canvas.remove(self.widget.selected_par)
                self.widget.selected_par = None 
        
        def cancel_pars(instance):
            #print('cancel parameter')
            self.input_pars.clear_widgets()
            self.option_pars.clear_widgets()
            
            #self.toolbox.remove_widget(self.input_pars)
            for par in self.list_input_pars:
                self.toolbox.remove_widget(par)
                
            self.list_input_pars.clear()
                
            self.toolbox.remove_widget(self.option_pars)
            self.toolbox.height = 200
            
            if self.widget.selected_par:
                self.widget.canvas.remove(self.widget.selected_par)
                self.widget.selected_par = None 
        
        
        btn_save = Button(text='Save')
        btn_save.bind(on_press=save_pars)
        btn_cancel = Button(text='Cancel')
        btn_cancel.bind(on_press=cancel_pars)
        
        
        self.option_pars.add_widget(btn_save)
        self.option_pars.add_widget(btn_cancel)
            
        
        self.toolbox.height = 250 + len(self.pars_dict)*50
        #self.toolbox.add_widget(self.input_pars)
        self.toolbox.add_widget(self.option_pars)
        