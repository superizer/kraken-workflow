# Code To Get Function Data From OpenCV Website
# Created By Attasuntorn Traisuwan

import re
import hashlib
import html
import json
from urllib import request
from .cvfunctions import Function,Parameter

# Open OpenCV Document From OpenCV Website

response = request.urlopen('http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html')        
#response = request.urlopen('http://docs.opencv.org/modules/imgproc/doc/filtering.html')
#response = request.urlopen('http://docs.opencv.org/modules/imgproc/doc/miscellaneous_transformations.html')
#response = request.urlopen('http://docs.opencv.org/modules/imgproc/doc/geometric_transformations.html')

htmls = response.read()

html_onespace = ' '.join(htmls.decode('utf-8').split())

html_onespace  = html.unescape(html_onespace)

func_name = 'func_name_not_found'
return_type = 'return_type_not_found'
parameters = []
descriptions = []
dic_funcs = {}

sections = re.findall(r'<div class="section" id="(((?!<h1>).)*?)">\s*(<h2>.*?)</ul>\s</td>',html_onespace)

for section in sections:
    
    funcs = re.findall(r'<dl class="function"> <dt id="(.*?)">',section[2])

    for fun in funcs:
	# Create Function Object To Store OpenCV Function By Function Name
        func_obj = Function(fun)
        func_obj.add_fname(section[0])

	# Store Function Description
        des = re.search(r'</h2>\s<p>(.*?)</p>\s<dl',section[2])
        func_obj.add_description(des.group(1))

        r_type = re.findall(r'^([\w\<\>]+) ([\w\<\>]+)\((.*)\)',fun)
        if r_type:
            for r in r_type:
                return_type = r[0]
                func_name = r[1]
                params = ' ' + r[2] + ','
                parameters = []
                pars = re.findall(r'\s(.*?),',params)
                for par in pars:
		            # Store Parameter And Parameter Return Type To Function Object
                    if par.count(' ') is 1:
                        par_pair = re.findall(r'(.*?)\s(.*)',par)
                        if par_pair:
                            func_obj.add_parameter_type(par_pair[0][1],par_pair[0][0])
                     
                    else:
                        par_three = re.findall(r'(.*?)\s(.*?)\s(.*)',par) 
                        if par_three:
                            func_obj.add_parameter_type(par_three[0][2],par_three[0][0] + ' ' + par_three[0][1])
		
		# Store Return Type Function To Function Object
                func_obj.add_return_type(return_type)
		
        set_desc = re.findall(r'<ul class="first last simple">.*',section[2])
        for set_des in set_desc:
            desc = re.findall(r'<strong>(.*?)</strong>(.*?)</li>',set_des)
            for des in desc:
		        # Store Parameter Description To Function Object
                func_obj.add_parameter_des(des[0],des[1])
	    # Store Function Object In Dictionary Structure
        dic_funcs[hashlib.md5(bytes(fun,'utf-8')).hexdigest()] = func_obj

# Print All Function Object In Dictionary Structure

cv = []

class FunctionJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Function): 
            return dict(name=obj.name,fname=obj.fname,return_type=obj.return_type,description=obj.description,pars=obj.pars,)
        elif isinstance(obj,Parameter):
            return dict(type=obj.type,name=obj.name,description=obj.description)
        return json.JSONEncoder.default(self, obj)

for fun in dic_funcs:
    cv.append(dic_funcs[fun])
    #print('Hash Function Name : ' + fun)
    #print(dic_funcs[fun])
    #print('\n\n')	
function = dict(cv=cv)
   
with open('/tmp/out.json', 'w') as f:
    json.dump(dict(function=function), f, cls=FunctionJsonEncoder)





