import json
import hashlib

from .cvfunctions import Function,Parameter
from kraken.json_parser.store_json import dic_funcs

'''dic_funcs = {}

with open("/tmp/out.json") as json_file:
    json_data = json.load(json_file)
    #print(json_data)
    funs = json_data['function']['cv']
    for fun in funs:
        #print(fun['name'])
        func_obj = Function(fun['name'])
        func_obj.add_fname(fun['fname'])
        func_obj.add_return_type(fun['return_type'])
        func_obj.add_description(fun['description'])
        for par in fun['pars']:
            func_obj.add_parameter_type(par['name'],par['type'])
            func_obj.add_parameter_des(par['name'],par['description'])
        dic_funcs[hashlib.md5(bytes(fun['name'],'utf-8')).hexdigest()] = func_obj
    
    for fun in dic_funcs:
        print('Hash Function Name : ' + fun)
        print(dic_funcs[fun])
        print('\n\n')'''
        
class Read_JSON():
    def __init__(self):
        self.dic_funcs = {}
        self.list_funcs = []
        
    def get_dic_funcs(self,library):
        with open("../cvlibrary/"+library) as json_file:
            json_data = json.load(json_file)
            funs = json_data['function']['cv']
            for fun in funs:
                #print(fun['name'])
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
        #print(self.list_funcs)
        return self.list_funcs
        
        #print(self.dic_funcs)
            
        '''for fun in self.dic_funcs:
            print('Hash Function Name : ' + fun)
            print(self.dic_funcs[fun])
            print('\n\n')'''
