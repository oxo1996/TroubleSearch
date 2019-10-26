from abc import *

class imodel(metaclass=ABCMeta):
    @abstractmethod
    def loadModel(self):
        pass
    
    @abstractmethod
    def saveModel(self):
        pass

    @abstractmethod
    def getData(self):
        pass