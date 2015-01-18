'''
Created on Jan 15, 2015

@author: superizer
'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class ParameterMenu():
    def __init__(self, pars_type,toolbox):
        self.pars_type = pars_type
        self.toolbox = toolbox
        self.input_pars = GridLayout(cols=2,size =(300,50))
        self.option_pars = GridLayout(cols=2,size =(300,50))
        
        
    def create_pars_layout(self):
        self.input_pars.add_widget(Label(text = 'Parameter1'))
        self.input_pars.add_widget(TextInput())
            
        def save_pars(instance):
            print('save pars')
            self.input_pars.clear_widgets()
            self.option_pars.clear_widgets()
            self.toolbox.remove_widget(self.input_pars)
            self.toolbox.remove_widget(self.option_pars)
            self.toolbox.height = 200
        
        def cancel_pars(instance):
            print('cancel parameter')
            self.input_pars.clear_widgets()
            self.option_pars.clear_widgets()
            self.toolbox.remove_widget(self.input_pars)
            self.toolbox.remove_widget(self.option_pars)
            self.toolbox.height = 200
            
        
        
        btn_save = Button(text='Save')
        btn_save.bind(on_press=save_pars)
        btn_cancel = Button(text='Cancel')
        btn_cancel.bind(on_press=cancel_pars)
        
        
        self.option_pars.add_widget(btn_save)
        self.option_pars.add_widget(btn_cancel)
            
        
        self.toolbox.height = 300
        self.toolbox.add_widget(self.input_pars)
        self.toolbox.add_widget(self.option_pars)
        