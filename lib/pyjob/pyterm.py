from datetime import datetime
from lazyme import string as lstring
import os

class PyTerm():
    
    log_file = None
    
    def __init__(self):
        pass
        
    @staticmethod
    def __log_colored__(msg, type, color):
        if PyTerm.log_file is None:
            return lstring.color_str('[ '+type.ljust(10," ") + " | " + str(datetime.now())+' | ' +str(os.getpid()).rjust(6, " ")+ ' ]', color)+' %s ' % msg
        return '[ '+type.ljust(10," ") + " | " + str(datetime.now())+' | ' +str(os.getpid()).rjust(6, " ")+ ' ] %s ' % msg
            
    @staticmethod 
    def __log_message(msg, type, color):
        msg = PyTerm.__log_colored__(msg, type, color)
        if PyTerm.log_file is None:
            print msg
        else: 
            with open(PyTerm.log_file, "a") as f:
                f.write(msg+"\n")
                f.close()
        
    @staticmethod 
    def log(msg):
        PyTerm.__log_message(msg, "LOG", "green");
        
    @staticmethod 
    def error(msg):
        PyTerm.__log_message(msg, "ERROR", "red");
        
    @staticmethod 
    def warning(msg):
        PyTerm.__log_message(msg, "WARNING", "yellow");
        
    @staticmethod 
    def setLogFile(file):
        PyTerm.log_file = file
        
    
