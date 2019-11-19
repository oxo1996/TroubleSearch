from abc import *

class iDetectReview(metaclass=ABCMeta):
    @abstractmethod
    def most_similar(symptom, reviews, num : int, order : str):
        pass