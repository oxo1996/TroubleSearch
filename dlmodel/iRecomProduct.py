from abc import *

class iRecomProduct(metaclass=ABCMeta):
    @abstractmethod
    def mostSimilar(symptom, product : str, num : int, order : str):
        pass

    @abstractmethod
    def recommendProduct(symptom):
        pass

    @abstractmethod
    def getResult(self, symptom, product : str):
        pass