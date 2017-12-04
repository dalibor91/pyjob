import json
import os

class JobProperties():
    
    __props__ = {}
    __props_file__ = ""
    
    def __init__(self, file):
        self.__props_file__ = file 
        self.reload()
        
    def reload(self):
        if os.path.isfile(self.__props_file__):
            with open(self.__props_file__) as fp:
                self.__props__ = json.load(fp)
        return self
                
    def flush(self):
        with open(self.__props_file__, 'w') as fp:
            fp.write(json.dumps(self.__props__, sort_keys=False, indent=4))
        return self
            
    def writeInMemory(self, key, val):
        self.__props__[key] = val 
        return self
    
    def write(self, key, val):
        return self.writeInMemory(key, val).flush() 
    
    def merge(self, obj):
        if isinstance(obj, dict):
            for k,v in obj.iteritems():
                self.writeInMemory(k, v)
        return self.flush()
    
    def read(self, key):
        if key in self.__props__:
            return self.__props__[key] 
        return None
        
    
