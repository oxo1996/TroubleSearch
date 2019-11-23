import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

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
        dup_dict = {}
        try:
            cursor = self._conn.cursor()
            cnt = 0
            for key in self.data.keys():
                # name = re.sub('\'', '년', key).lower()  이름 변경 안한 것
                name = key
                if name not in dup_dict.keys():
                    # query = "insert into item (id, name) values ("+str(cnt)+', \"'+name+'\")'
                    query = """insert into item (id, name) values (%s, %s)"""
                    print(query, (cnt, name))
                    cursor.execute(query, (cnt, name))
                    self._conn.commit()
                    cnt += 1
                    dup_dict[name] = 1

        finally:
            self._conn.close()
