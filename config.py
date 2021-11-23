from configparser import ConfigParser
from pprint import pprint
#reading the config file

class Data():
    '''
    Return a set of coulmns from a config file that will be displayed
    Path = path of the configuration file
    '''
    def __init__(self,path) -> None:
        self.path = path
    def fields(self):
        config = ConfigParser()
        config.read(self.path)
        #finding the fields that needs to be displayed
        keys = []
        if 'Idnumber' not in (config['Fields'])or config['Fields']['Idnumber']=='no':
            keys.append('IDNUMBER')
            #print(config.options('Fields'))
        for key,value in config.items(config.sections()[0]):
            if value == 'yes':
                keys.append(str(key).upper().strip())
        return keys
    def fpath(self):
        config = ConfigParser()
        config.read(self.path)
        for key,value in config.items(config.sections()[-1]):
            #print(key,value)
            if key == 'PathtoDataFile'.lower():
                #print(value)
                return value
            else:
                return None
#print(Data('config.ini').fpath())    