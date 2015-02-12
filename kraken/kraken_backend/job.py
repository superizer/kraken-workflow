import queue

class Job(object):
    def __init__(self,priority,thread):
        self.priority = priority
        self.thread = thread
        #print('New job:', thread)
    def __cmp__(self,other):
        return cmp(self.priority, other.priority)
    def __lt__(self, other):
        return self.priority < other.priority
    def __gt__(self, other):
        return self.priority > other.priority
    def __le__(self, other):
        return self.priority <= other.priority
    def __ge__(self, other):
        return self.priority >= other.priority


'''q = queue.PriorityQueue()

q.put(Job(1,'aaa'))
q.put(Job(-1,'bbb'))
q.put(Job(0,'ccc'))


while not q.empty():
    next_job = q.get()
    print('Processing job',next_job.thread)'''

