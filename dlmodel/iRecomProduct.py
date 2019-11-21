from abc import *

class iRecomProduct(metaclass=ABCMeta):
    @abstractmethod
    def most_similar(symptom, product : str, num : int, order : str):
        pass

    @abstractmethod
    def recommend_product(symptom):
        pass

    @abstractmethod
    def get_result(self, symptom, product : str):
        pass