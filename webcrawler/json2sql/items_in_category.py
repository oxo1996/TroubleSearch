import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

from json2sql import iJson2Sql
import pymysql
import json
import re


class ItemsInCategory(iJson2Sql):
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
            query = "select * from item"
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                rid = row[0]
                # name = re.sub('년', '\'', row[1])   이름 변경 안한 것
                name = row[1]
                cat = self.data[name]["categories"]

                # query = "insert into items_in_category (item_id, category_id) \nvalues (" + str(
                #     rid) + ', ' + "\n(select id from category where name=" + "\'" + cat + "\'" + '))'

                query = """insert into items_in_category (item_id, category_id)
                values (%s, (select id from category where name = %s))"""

                # print(query)
                cursor.execute(query, (rid, cat))
                self._conn.commit()
        finally:
            self._conn.close()
