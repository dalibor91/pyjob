from lib import PyJob 
from lib import PyTerm
import time

class DummyJob(PyJob):    
            
    def onStart(self):
        PyJob.onStart(self)
        self.lockProcess()
            
    def hello(self):
        PyTerm.log("Hi from %s" % self.job_name)
        time.sleep(60)
        PyTerm.log("Bye from %s" % self.job_name)
        
    def handle(self):
        PyJob.handle(self);
        self.hello();
        
    def shouldRun(self, last_run):
        if self.isProcessLocked():
            PyTerm.warning("Process is locked ....")
            return False
        return True;
