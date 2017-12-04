from pyterm import PyTerm
from jobproperties import JobProperties
import sys
import os
import time

class PyJob(object):
    
    __props_file__  = None
    
    job_name   = ''
    lock_file  = ''
    log_file   = ''
    
    def __init__(self, name=''):
        self.job_name = name
        self.lock_file = "%s/storage/locks/%s.lock" % (os.getenv('APP_ROOT'), name)
        self.log_file = "%s/storage/logs/%s.log" % (os.getenv('APP_ROOT'), name)
        
        self.properties().merge({
            "init_time": time.time(),
            "lock_file": self.lock_file, 
            "log_file" : self.log_file,
            "finished": False, 
            "failed" : False
        });
        
        PyTerm.log("__init__(%s)" % self.job_name);

    def onStart(self):
        PyTerm.log("onStart(%s)" % self.job_name);
        self.properties().write("last_pid", os.getpid());
        
    def onFail(self, e=None):
        PyTerm.log("onFail(%s)" % self.job_name);
        self.unlockProcess();

        self.properties().merge({
            "fail_time": time.time(), 
            "done_time": time.time(),
            "failed" : True,
            "finished": True, 
            "fail_msg": str(e) 
        })
        
        sys.exit(1)
        
    def onFinish(self):
        PyTerm.log("onFinish(%s)" % self.job_name);
            
        self.properties().merge({
            "done_time" : time.time(), 
            "finished": True
        });
        self.unlockProcess();
        
        sys.exit(0)
        
    def handle(self):
        PyTerm.log("handle(%s)" % self.job_name);
        
    def shouldRun(self, last_run):
        return False
    
    def properties(self):
        if self.__props_file__ is None:
            self.__props_file__ = JobProperties("%s/storage/props/%s.json" % (os.getenv('APP_ROOT'), self.job_name))
        return self.__props_file__;

    def getLogFile(self):
        return self.log_file
    
    def lockProcess(self):
        with open(self.lock_file, "w") as f:
            f.write(str(os.getpid()))
            f.close()
    
    def unlockProcess(self):
        PyTerm.log("unlockProcess(%s)" % self.job_name)
        if os.path.isfile(self.lock_file):
            os.unlink(self.lock_file)
    
    def isProcessLocked(self):
        return os.path.isfile(self.lock_file)
