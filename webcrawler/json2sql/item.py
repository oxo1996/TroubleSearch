from json2sql import iJson2Sql
import pymysql
import json
import re


class Item(iJson2Sql):
    def __init__(self, path):
        self._jsonpath = path
        self._conn = pymysql.connect(host='localhost', user='root', password='rhwk6925', db='tsdb', charset='utf8')    
        self.data = self._read_data()

    def _read_data(self):
        with open(self._jsonpath) as json_file:
            data = json.load(json_file)
        return data

    def insert_data(self):
        try:
            cursor = self._conn.cursor()
            cnt = 0
            for key in self.data.keys():
                name = re.sub('\'', '년', key)
                query = "insert into item (id, name, brand) values ("+str(cnt)+', \''+name+'\', \''+self.data[key]["brand"]+'\')'
                print(query)
                cursor.execute(query)
                self._conn.commit()
                cnt += 1
        finally:
            self._conn.close()