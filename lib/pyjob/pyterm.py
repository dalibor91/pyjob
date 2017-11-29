from datetime import datetime
from lazyme import string as lstring
import os

class PyTerm():
    def __init__(self):
        pass
        
    @staticmethod
    def __log_colored__(msg, type, color):
        return lstring.color_str('[ '+type.ljust(10," ") + " | " + str(datetime.now())+' | ' +str(os.getpid()).rjust(6, " ")+ ' ]', color)+' %s ' % msg
        
    @staticmethod 
    def log(msg):
        print PyTerm.__log_colored__(msg, "LOG", "green");
        
    @staticmethod 
    def error(msg):
        print PyTerm.__log_colored__(msg, "ERROR", "red");
        
    @staticmethod 
    def warning(msg):
        print PyTerm.__log_colored__(msg, "WARNING", "yellow");
        
    
