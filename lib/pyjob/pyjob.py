from pyterm import PyTerm
import sys
import os
import time

class PyJob(object):
    
    job_name   = ''
    lock_file  = ''
    time_file  = ''
    last_start = 0
    current_start = 0
    
    def __init__(self, name=''):
        self.job_name = name
        self.current_start = time.time()
        self.lock_file = "%s/storage/locks/%s.lock" % (os.getenv('APP_ROOT'), name)
        self.time_file = "%s/storage/run/%s.time-start" % (os.getenv('APP_ROOT'), name)
        
        if os.path.isfile(self.time_file):
            with open(self.time_file, "r") as tf:
                str = tf.read()
                self.last_start = float(0 if str == "" else float(str))
        
        PyTerm.log("__init__(%s)" % self.job_name);

    def onStart(self):
        PyTerm.log("onStart(%s)" % self.job_name);
        with open(self.lock_file, "w") as f:
            f.write(str(os.getpid()))
        
    def onFail(self, e=None):
        PyTerm.log("onFail(%s)" % self.job_name);
        if os.path.isfile(self.lock_file):
            os.unlink(self.lock_file)

        with open(self.time_file, "w") as tf:
            tf.write(str(self.current_start))
        
    def onFinish(self):
        PyTerm.log("onFinish(%s)" % self.job_name);
        if os.path.isfile(self.lock_file):
            os.unlink(self.lock_file)
            
        with open(self.time_file, "w") as tf:
            tf.write(str(self.current_start))
        sys.exit(0)
        
    def handle(self):
        PyTerm.log("handle(%s)" % self.job_name);
        
    def shouldRun(self, last_run):
        return False
