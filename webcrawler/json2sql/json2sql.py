import pymysql.cursors
from abc import *

class json2sql(metaclass=ABCMeta):
    @abstractmethod  
    def makeDB(self, name):
        pass

    @abstractmethod
    def makeTable(self, name):
        pass

    @abstractmethod
    def insertData(self):
        pass