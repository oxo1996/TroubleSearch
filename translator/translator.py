from abc import *

class translator(metaclass=ABCMeta):
    @abstractmethod
    def translate(self):
        pass