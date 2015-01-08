import json
import hashlib

from cvfunctions import Function,Parameter

dic_funcs = {}

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
        print('\n\n')

