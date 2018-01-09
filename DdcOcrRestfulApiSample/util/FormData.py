class FormData:
    def __init__(self):
        self.__listFormData = []
        
    def append(self, strKey, value, strFileName=None):
        self.__listFormData.append((strKey, value, strFileName))
    
    def clear(self):
        del self.__listFormData[:]
        
    def isValid(self):
        return not(self.__listFormData is None)
    
    def getAll(self):
        return self.__listFormData