from pyjob import PyJob
from pyterm import PyTerm
from jobscanner import JobScanner
import datetime 
import os
import sys

MAX_PROCESSES= 40

def start_job(dir, module, rest):
    PyTerm.log("start_job(%s)" % dir);
    scanner = JobScanner(dir)
    
    defcls = scanner.get_job_class(module)
    if defcls is None:
        PyTerm.error("%s does not have PyJob class" % module)
        return False
    
    if not defcls.shouldRun():
        PyTerm.warning("shouldRun returned True, %s should not run" % module)
        try :
            rest.index('-f')
        except:
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
                PyTerm.error("%s does not have PyJob class." % module)
                continue 
            
            if defcls.shouldRun():
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
        
def run_new(dir, commands):
    if len(commands) > 1:
        PyTerm.error("Only one command after 'new' command")
        return False 
    
    if len(commands) == 0:
        PyTerm.error("Name should be passed also")
        return False
    
    if os.path.isdir("%s/%s" %(dir, commands[0])):
        PyTerm.error("Directory in %s with name '%s' already exists." %(dir, commands[0]))
        return False;
    
    if os.path.isfile("%s/%s" %(dir, commands[0])):
        PyTerm.error("File in %s with name '%s' already exists." %(dir, commands[0]))
        return False;
    
    import re 
    if re.search('[^a-z0-9\-_]', commands[0], flags=re.IGNORECASE):
        PyTerm.error("Name of job can consist of numbers, letters (a-zA-z), '-', '_' ")
        return False
    
    try: 
        os.mkdir("%s/%s"%(dir, commands[0]))
        file = "%s/%s/__init__.py"%(dir, commands[0])
        className=""
        
        for part in re.split('[-_]', commands[0], flags=re.IGNORECASE):
            className = "%s%s" % (className, part.lower().title())
        
        className="%sJob"%className
        
        with open(file, 'w') as fp:
            fp.write(''' 
# Generated: %s

from lib import PyJob 
from lib import PyTerm

class %s(PyJob):
    def onStart(self):
        #this is executed before self.handle() method
        PyJob.onStart(self);
        
    def handle(self):
        #actial code of cronjob 
        PyJob.handle(self);
    
    def onFail(self):
        #handling data on fail 
        PyJob.onFail(self);
        
    def shouldRun(self):
        #when should run 
        return False
    
            '''.strip() % (str(datetime.datetime.now()), className) );
            fp.close()
            PyTerm.log("Generated %s" % file)
    except Exception, e:
        PyTerm.error("We have an error")
        PyTerm.error(str(e))
        
        
def print_help():
    print ('''

PyJob is small project that 
allows you to create python modules that 
will be runned after some time 

Commands:
    list             -  List availible jobs 
    run      [-f]    -  Run specific job , use flag -f for force
    new      <name>  -  Generates new job
    all              -  Run all jobs 
    cleanup          -  Cleans logs and locks
'''.strip())


def run_command(command, rest_commands, dir):
    if command == 'list':
        print_jobs("%s/jobs" % dir)
    elif command == 'all':
        start_jobs("%s/jobs" % dir)
    elif command == 'cleanup':
        run_cleanup(dir)
    elif command == 'new' and len(rest_commands) > 0:
        run_new("%s/jobs" % dir, rest_commands);
    elif command == 'run' and len(rest_commands) > 0:
        start_job("%s/jobs" % dir, rest_commands[0], rest_commands[1:])
    else:
        print_help()
