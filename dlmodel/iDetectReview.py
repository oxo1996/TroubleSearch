from abc import *

class iDetectReview(metaclass=ABCMeta):
    @abstractmethod
    def mostSimilar(symptom, reviews, num : int, order : str):
        pass