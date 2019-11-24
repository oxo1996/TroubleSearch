import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

import pymysql.cursors
from abc import *


class iJson2Sql(metaclass=ABCMeta):
    @abstractmethod
    def _read_data(self):
        pass

    @abstractmethod
    def insert_data(self):
        pass
