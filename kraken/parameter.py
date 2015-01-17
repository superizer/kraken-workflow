'''
Created on Jan 15, 2015

@author: superizer
'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class ParameterMenu():
    def __init__(self, pars_dict):
        self.pars_dict = pars_dict
        
    def pars_layout(self):
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