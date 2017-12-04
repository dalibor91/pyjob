from pyjob import PyJob
from pyterm import PyTerm
from jobscanner import JobScanner
import os

MAX_PROCESSES=40

def start_jobs(dir):
    PyTerm.log("start_jobs(%s)" % dir);
    scanner = JobScanner(dir)
    
    counter=0;
    
    for module in scanner.get_modules():
        PyTerm.log("Load module %s" % module)
        try :
            defcls = scanner.get_job_class(module)
            
            if (defcls.shouldRun(0)):
                counter+=1
                PyTerm.log("Running module %s" % module)
                
                if os.fork() == 0:
                    PyTerm.setLogFile(defcls.getLogFile())
                    defcls.onStart()
                    defcls.handle()
                    defcls.onFinish()
            else:
                PyTerm.warning("Module should not run")
        except Exception, e:
            PyTerm.error(str(e));
            if 'defcls' in vars():
                defcls.onFail(e)
                
        if counter == MAX_PROCESSES:
            break
    
