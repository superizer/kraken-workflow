'''
Created on Jan 15, 2015

@author: superizer
'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class Parameter():
    def __init__(self, pars_dict):
        self.pars_dict = pars_dict
        
    def get_pars_layout(self):
        pass
    
    def save_pars(self,instance):
        print('save parameter')
        self.input_pars.clear_widgets()
        self.option_pars.clear_widgets()
        self.parent.tool_box.remove_widget(self.input_pars)
        self.parent.tool_box.remove_widget(self.option_pars)
        self.parent.tool_box.height = 150
        
    def cancel_pars(self,instance):
        print('cancel parameter')
        self.input_pars.clear_widgets()
        self.option_pars.clear_widgets()
        self.parent.tool_box.remove_widget(self.input_pars)
        self.parent.tool_box.remove_widget(self.option_pars)
        self.parent.tool_box.height = 150