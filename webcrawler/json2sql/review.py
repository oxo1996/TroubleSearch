import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

from json2sql import iJson2Sql
import pymysql
import json
import re
from pymysql.err import InternalError


class Review(iJson2Sql):
    def __init__(self, path):
        self._jsonpath = path
        self._conn = pymysql.connect(host='localhost', user='root', password='rhwk6925', db='tsdb', charset='utf8')
        self.data = self._read_data()

    def _read_data(self):
        with open(self._jsonpath) as json_file:
            data = json.load(json_file)
        return data

    def _find_item_id(self, pname):
        cursor = self._conn.cursor()
        query = "select id from item where name = \"" + pname + '\"'
        cursor.execute(query)
        pid = cursor.fetchone()

        return pid

    def insert_data(self):
        try:
            cursor = self._conn.cursor()
            cnt = 0
            for pname in self.data.keys():
                # item_table_name = re.sub('\'', '년', pname)
                # pid = self._find_item_id(item_table_name)
                pid = self._find_item_id(pname)
                # print(pid, pname)
                reviews = self.data[pname]["reviews"]
                try:
                    for review in reviews:
                        try:
                            # print(review[1])
                            content = re.sub('[\'\";]', '', review[1])
                            query = "insert into review(id, score, content) \nvalues (" + str(cnt) + ', ' + str(
                                review[0]) + ', \'' + \
                                    content + '\');' + "\ninsert into reviews_in_item(review_id, item_id) values (" + str(
                                cnt) + ', ' + str(pid[0]) + ');'

                            print(cnt)

                            # print(query)
                            for stmt in query.split(';'):
                                if stmt.strip():
                                    print(stmt)
                                    cursor.execute(stmt)
                                    self._conn.commit()
                            cnt += 1
                        except InternalError as e:
                            print(e)
                            print(review)
                            continue
                except TypeError as e:
                    print(e)
                    continue
        finally:
            self._conn.close()
