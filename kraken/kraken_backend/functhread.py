import threading
import time
from cv2 import *
from mapqueue import MapQueue
 
class FuncThread(threading.Thread):
    def __init__(self, target = None, args=(), kwargs=None, in_cv_q=(), out_cv_q=(),uid = None):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.in_cv_q = in_cv_q
        self.out_cv_q = out_cv_q
        self.uid = uid
        self.time = None
 
    def run(self):
        #print(self.target, self.args)
        kwargs = {}
        for par in self.kwargs.items():
            #if par[0] == 'params':
            #    del self.kwargs
            #print('par',par,' ',par[1][0:3])
            kwargs[par[0]] = par[1]
            #print("check type: ", type(par[1]) is str and par[1][0:3] == 'id=')
            if type(par[1]) is str and par[1][0:3] == 'id=':
                #print('yes')
                while MapQueue.queues[par[1][3:],self.uid].empty():
                    time.sleep(0.5)    
                p = MapQueue.queues[par[1][3:],self.uid].get()
                kwargs[par[0]] = p 
        '''if 'params' in kwargs:
            del kwargs['params']'''
        kwargs = dict((k, v) for k, v in kwargs.items() if v != '')
        #print('kwargs',kwargs)
        #print(kwargs)
        t0 = time.clock()
        output = self.target(**kwargs)
        self.time = round((time.clock() - t0)*1000,4)
        
        #print(self.target,'output',output)
        if self.target == imwrite or self.target == putText:
            imwrite('/tmp/images/' + self.uid + '.jpg',kwargs['img'])
            
        else:
            imwrite('/tmp/images/' + self.uid + '.jpg',output)
        for i  in self.out_cv_q:
            MapQueue.queues[self.uid,i].put(output)

 
# Example usage
'''def someOtherFunc(data, key):
    #print "someOtherFunc was called : data=%s; key=%s" % (str(data), str(key))
    print(str(data) + ' ' + str(key))
 
t1 = FuncThread(target = someOtherFunc, kwargs = {'key': 6,'data': [1,2]})
t1.start()
t1.join()'''
