from cv2 import *
import sys
import json
import os
import glob
import threading
import queue
from mapqueue import MapQueue
from job import Job
from functhread import FuncThread

#print(sys.argv[1])

if __name__ == "__main__":
    
    #remove file
    files = glob.glob('/tmp/images/*.jpg')
    for f in files:
        os.remove(f)

    #f = str(sys.argv[1])
    #map_queue = {}
    thread_queue = queue.PriorityQueue()
    
    #with open(f) as json_file:
    json_file = input()
    if json_file:
        #json_data = json.load(json_file)
        json_data = json.loads(json_file)
        funs = json_data['workflow']['cv']
        for fun in funs:
            if fun['name'] != 'Line':
                dic_param = {}
                for par in fun['pars']:
                    if par['value'] != '':
                        if par['type'] == 'int':
                            if len(par['value']) > 6 and (par['value'][0:6] == "COLOR_" or par['value'][0:3] == "cv2"):
                                if par['value'][0:6] == "COLOR_":
                                    par['value'] = 'cv2.' + par['value']
                                par['value'] = eval(par['value'])
                            else:
                                par['value'] = int(par['value'])
                        elif par['type'] == 'double' or par['type'] == 'float':
                            par['value'] = float(par['value'])
                        else:
                            #parr['value'] = par_value
                            try:
                                v = eval(par['value'])
                            except:
                                v = par['value']
                            par['value'] = v
                    dic_param[str(par['name'])] = par['value']
                #print('dic_param ' + str(dic_param))
            
                for i in fun['out_cv']:
                    #print('map',str(fun['id']),str(i))
                    #map_queue[str(fun['id']),str(i)] = queue.Queue()
                    MapQueue.queues[str(fun['id']),str(i)] = queue.Queue()

                t = FuncThread(target = eval(fun['name']),kwargs = dic_param, in_cv_q = fun['in_cv'], out_cv_q = fun['out_cv'],uid = fun['id'])
                #print(fun['level'])
                thread_queue.put(Job(fun['level'],t))
                
        if not os.path.exists('/tmp/images'):
            os.makedirs('/tmp/images')

        while not thread_queue.empty():
            t = thread_queue.get()
            t.thread.start()
            t.thread.join()
    response = dict(status = 'Success')
    print(response)





