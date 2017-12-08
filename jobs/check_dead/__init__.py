from lib import PyJob 
from lib import PyTerm
import glob
import os 
import time

class CheckdeadJob(PyJob):   
    def onStart(self):
        PyJob.onStart(self)
        self.lock().lock()
        
    def handle(self):
        PyJob.handle(self);
        for file in glob.glob("%s/storage/locks/*.lock" % os.getenv('APP_ROOT')):
            remove = False
            with open(file, "r") as fp:
                pid = int(fp.read()) 
                
                try:
                    os.kill(pid, 0)
                except OSError:
                    PyTerm.warning("Process %d does not exists, removing file %s" % (pid, file))
                    remove = True
                
                fp.close()
            
            if remove:
                os.unlink(file)
                
        
    def shouldRun(self):
        if self.lock().isActive():
            return False
        
        last_done    = self.properties().read('done_time')
        failed       = self.properties().read('failed')
        current_time = time.time()
        
        if last_done is None:
            return True 
        
        if failed:
            # retry after fail 
            if current_time - last_done > 300:
                return True 
            # retry after success
        elif current_time - last_done > 600:
            return True
        
        return False;
