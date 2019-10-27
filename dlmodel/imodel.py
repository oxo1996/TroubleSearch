from abc import *

class imodel(metaclass=ABCMeta):
    @abstractmethod
    def mostSimilar(symptom : str, product : str, num : int, order : str):
        pass

    @abstractmethod
    def getResult(self, symptom : str, product : str):
        pass