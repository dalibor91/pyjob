import os
import importlib
import inspect
from types import ModuleType
from pyjob import PyJob

class JobScanner():
    def __init__(self, directory):
        self.directory = directory
        
    def get_modules(self, directory="", append=""):
        modules = []
        directory = directory if directory else self.directory
        
        for path in os.listdir(directory):
            if os.path.isfile("%s/%s/__init__.py" % (directory, path)):
                _append="%s.%s" % (append, path)
                modules.append(_append.strip('.'))

                for sub in self.get_modules("%s/%s" % (directory, path), _append.strip('.') ):
                    modules.append(sub)
        return modules
        
    def load_module(self, name):
        if self.get_modules().index(name) >= 0:
            return importlib.import_module("jobs.%s" % name)
        return None
        
    def get_job_class(self, _module):
        module = self.load_module(_module)
        if isinstance(module, ModuleType):
            for i in dir(module):
                if i == 'PyJob' or not i.endswith('Job'):
                    continue
                
                attr = getattr(module, i)
                
                if not inspect.isclass(attr):
                    continue
                
                attr_cls = attr(_module);
                
                if isinstance(attr_cls, PyJob):
                    return attr_cls
        return None
