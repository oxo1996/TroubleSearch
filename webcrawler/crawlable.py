from abc import *


class crawlable(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self):
        pass
