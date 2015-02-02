'''
Created on Jan 15, 2015

@author: superizer
'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class InputForm(TextInput):
    
    def __init__(self,toolbox,  **kwargs):
        self.toolbox = toolbox
        super(InputForm, self).__init__(**kwargs)
        
    def on_double_tap(self):
        #print('hello tappp !!')
        ds = self.toolbox.drawing_space
        for child in ds.children:
            if child.selected:
                #print('select :',child.id)
                self.text = 'id=' + child.id

class ParameterMenu():
    def __init__(self, pars_dict,toolbox):
        self.pars_dict = pars_dict
        self.toolbox = toolbox
        self.input_pars = GridLayout(cols=2,size =(300,50))
        self.option_pars = GridLayout(cols=2,size =(300,50))
        self.list_input_pars = []
        
    def create_pars_layout(self):
        
        #self.input_pars.add_widget(Label(text = 'Parameter1'))
        #self.input_pars.add_widget(TextInput())
        
        self.input_pars = GridLayout(cols=2,size =(300,50*len(self.pars_dict)))
        
        for par in self.pars_dict:
            #self.input_pars.add_widget(Label(text = 'Parameter1'))
            #self.input_pars.add_widget(TextInput())
            self.input_pars = GridLayout(cols=2,size =(300,50))
            self.input_pars.add_widget(Label(text = par['name']))
            #self.input_pars.add_widget(TextInput(text=par['value']))
            
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
                    if parr['name'] == par_name:
                        if parr['type'] == 'int':
                            parr['value'] = int(par_value)
                        elif parr['type'] == 'double' or parr['type'] == 'float':
                            parr['value'] = float(par_value)
                        else:
                            parr['value'] = par_value
                
                self.toolbox.remove_widget(par)
            
            self.list_input_pars.clear()
            self.input_pars.clear_widgets()
            self.option_pars.clear_widgets()
            
            self.toolbox.remove_widget(self.option_pars)
            self.toolbox.height = 200
        
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
            
        
        
        btn_save = Button(text='Save')
        btn_save.bind(on_press=save_pars)
        btn_cancel = Button(text='Cancel')
        btn_cancel.bind(on_press=cancel_pars)
        
        
        self.option_pars.add_widget(btn_save)
        self.option_pars.add_widget(btn_cancel)
            
        
        self.toolbox.height = 250 + len(self.pars_dict)*50
        #self.toolbox.add_widget(self.input_pars)
        self.toolbox.add_widget(self.option_pars)
        