# Generated: 2017-12-08 12:46:23.557726

from lib import PyJob 
from lib import PyTerm

import time
import datetime

class DummyJob(PyJob):
    def onStart(self):
        #this is executed before self.handle() method
        PyJob.onStart(self);
        self.lock().lock()
        
    def handle(self):
        #actial code of cronjob 
        PyJob.handle(self);
        PyTerm.log("Sleeping started %s" % str(datetime.datetime.now()))
        time.sleep(120)
        PyTerm.log("Sleeping ended %s" % str(datetime.datetime.now()))
    
    def onFail(self):
        #handling data on fail 
        PyJob.onFail(self);
        
    def shouldRun(self):
        #when should run
        if self.lock().isActive(): 
            return False
        return True
