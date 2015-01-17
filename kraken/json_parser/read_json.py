import json
import hashlib

from .cvfunctions import Function, Parameter
        
class CVFunctionParser():
    def __init__(self, path):
        self.dic_funcs = {}
        self.list_funcs = []
        self.path = path
        
    def get_from_json(self,library):
        with open(self.path + '/' + library) as json_file:
            json_data = json.load(json_file)
            funs = json_data['function']['cv']
            for fun in funs:
                #print(fun['fname'])
                func_obj = Function(fun['name'])
                func_obj.add_fname(fun['fname'])
                self.list_funcs.append(fun['fname'])
                func_obj.add_return_type(fun['return_type'])
                func_obj.add_description(fun['description'])
                for par in fun['pars']:
                    func_obj.add_parameter_type(par['name'],par['type'])
                    func_obj.add_parameter_des(par['name'],par['description'])
                self.dic_funcs[hashlib.md5(bytes(fun['name'],'utf-8')).hexdigest()] = func_obj
        
    def get_list_funs(self):
        return self.list_funcs
    
    def get_pars_in_funcs(self,func):
        pars = []
        for fun in self.dic_funcs.values():
            p = {}
            if fun.fname == func and len(fun.pars) != 0:
                for par in fun.pars:
                    p['type'] = par.type
                    p['name'] = par.name
                    p['description'] = par.description
                pars.append(p)
                break
        return pars
    
    def get_pars_type(self,func):
        pars = []
        for fun in self.dic_funcs.values():
            p = []
            if fun.fname == func:
                for par in fun.pars:
                    p.append(par.type) 
                pars.append(str(p))
        return pars
            
        
                
    
    
