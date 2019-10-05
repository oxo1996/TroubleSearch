from abc import *

class crawlable(metaclass=ABCMeta):
    @abstractmethod
    def getData(self):
        pass