from pyjob import PyJob
from pyterm import PyTerm
from jobscanner import JobScanner
from time import sleep
import os
import sys

MAX_PROCESSES= 40

def start_job(dir, module):
    PyTerm.log("start_job(%s)" % dir);
    scanner = JobScanner(dir)
    
    defcls = scanner.get_job_class(module)
    if defcls is None:
        PyTerm.error("%s does not have PyJob class" % module)
        return False
    
    if not defcls.shouldRun(0):
        PyTerm.warning("%s should not run" % module)
        return False
    
    try:
        defcls.onStart()
        defcls.handle()
        defcls.onFinish()
    except Exception, e:
        PyTerm.error(str(e));
        if 'defcls' in vars():
            defcls.onFail(e)
        sys.exit(1)
    sys.exit(0)


def start_jobs(dir):
    PyTerm.log("start_jobs(%s)" % dir);
    scanner = JobScanner(dir)
    
    counter=0;
    
    for module in scanner.get_modules():
        PyTerm.log("Load module %s" % module)
        
        try :
            defcls = scanner.get_job_class(module)
            if defcls is None:
                PyTerm.error("%s does not have PyJob class" % module)
                continue 
            
            if defcls.shouldRun(0):
                counter+=1
                PyTerm.log("Running module %s" % module)
                
                if os.fork() == 0:
                    PyTerm.setLogFile(defcls.getLogFile())
                    defcls.onStart()
                    defcls.handle()
                    defcls.onFinish()
                    sys.exit(0)
            else:
                PyTerm.warning("Module should not run")
        except Exception, e:
            PyTerm.error(str(e));
            if 'defcls' in vars():
                defcls.onFail(e)
                
        if counter == MAX_PROCESSES:
            break


def print_jobs(dir):
    scanner = JobScanner(dir)
    print("Availible jobs:\n");
    for module in scanner.get_modules():
        print "- %s" % module

def run_cleanup(dir):
    import glob

    for file in glob.glob("%s/storage/locks/*.lock" % dir):
        PyTerm.log("Removing %s" % file)
        os.unlink(file)

    for file in glob.glob("%s/storage/logs/*.log" % dir):
        PyTerm.log("Removing %s" % file)
        os.unlink(file)
        
    for file in glob.glob("%s/storage/props/*.json" % dir):
        PyTerm.log("Removing %s" % file)
        os.unlink(file)
        
def print_help():
    print ('''

PyJob is small project that 
allows you to create python modules that 
will be runned after some time 

Commands:
    list        - List availible jobs 
    run         - Run specific job 
    all         - Run all jobs 
    cleanup     - Cleans logs and locks
'''.strip())


def run_command(command, rest_commands, dir):
    if command == 'list':
        print_jobs("%s/jobs" % dir)
    elif command == 'all':
        start_jobs("%s/jobs" % dir)
    elif command == 'cleanup':
        run_cleanup(dir)
    elif command == 'run' and len(rest_commands) > 0:
        start_job("%s/jobs" % dir, rest_commands[0])
    else:
        print_help()
