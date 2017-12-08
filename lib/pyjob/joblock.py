import os

class JobLock():
    
    file = None
    pid = None
    
    def __init__(self, file):
        self.file = file
        if self.lockExists():
            self.getPID()

    def lockExists(self):
        return os.path.isfile(self.file)
    
    def isActive(self):
        pid = self.getPID()
        
        if pid is None:
            return False
        
        try :
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    
    def getPID(self, reload=False):
        if not self.lockExists():
            return None
        
        if self.pid is None or reload:
            with open(self.file, 'r') as fp:
                self.pid = int(fp.read())
                fp.close();
            
        return self.pid 
    
    def unlock(self):
        if self.lockExists():
            os.unlink(self.file)
            self.pid = None
            
    def lock(self):
        if not self.lockExists():
            with open(self.file, 'w') as fp:
                fp.write(str(os.getpid()))
                fp.close()
            
            if not self.getPID():
                raise Error("ERROR: Unable to get PID")
            
            if not self.isActive():
                raise Error("ERROR: Got process is not active")
    
    
        
