from lib import PyJob 
from lib import PyTerm
import time

class DummyJob(PyJob):    
            
    def hello(self):
        PyTerm.log("Hi from %s" % self.job_name)
        time.sleep(16)
        PyTerm.log("Bye from %s" % self.job_name)
        
    def handle(self):
        PyJob.handle(self);
        self.hello();
        
    def shouldRun(self, last_run):
        return True;
