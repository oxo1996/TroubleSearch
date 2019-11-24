from abc import *


class iEmbedding(metaclass=ABCMeta):
    @abstractmethod
    def _preprocess(self):
        pass

    @abstractmethod
    def calc_vec(self):
        pass

    @abstractmethod
    def most_similar(self, symptom, reviews, num: int, order: str):
        pass
