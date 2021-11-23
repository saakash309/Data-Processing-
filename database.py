class Database():
    def __init__(self, dictio):
        for k, v in dictio.items():
            self.__dict__[k] = v

    # def from_file(self,name,value):
    #     setattr(self,str(name),value)
def attr_type(value):
    try:
        int(value)
        return 'int'
    except ValueError:
        return 'str'

def data_columns(keys,file_path):
    '''  
    Gets the fields from config file and reads the txt file and returns a list of objects which are instance of the database class
    '''
    list_objects = []
    dictionary = {}
    #reading the txt file
    ftr = open(file_path)
    while True:
        line= ftr.readline().strip()
        if line == '':
            break
        if len(keys) == len(line.split(';')):
            for key,value in (list(zip(keys,line.split(';')))):                                                                        
                dictionary[key] = value  
            list_objects.append(Database(dictionary))                      
            dictionary = {}
        else:
            array = line.split(';')
            array.append('-')
            for i in range(len(keys)-len(array)):
                array.append('-')
            for key,value in (list(zip(keys,array))):                                                                        
                dictionary[key] = value  
            list_objects.append(Database(dictionary))                      
            dictionary = {}
    return list_objects

def add_data(line,fname):
    '''
    Adds new value to the files
    '''
    with open(fname,'a') as f:
        f.write(f'{line}\n')