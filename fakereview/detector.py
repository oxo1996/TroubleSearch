from abc import *


class detector(metaclass=ABCMeta):
    @abstractmethod
    def predict(self):
        pass
