import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

from json2sql import iJson2Sql
import pymysql
import json
import re


class ItemsInBrand(iJson2Sql):
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
            query1 = "select * from item"
            cursor.execute(query1)
            rows = cursor.fetchall()

            for row in rows:
                rid = row[0]
                # name = re.sub('년', '\'', row[1]).lower()   이름 변경 안한 것
                name = row[1]
                brand = self.data[name]["brand"]

                # query2 = "insert into items_in_brand (item_id, brand_id) \nvalues (" + str(
                #     rid) + ', ' + "\n(select id from brand where name=" + "\'" + brand + "\'" + '))'
                query2 = """insert into items_in_brand (item_id, brand_id)
                values (%s, (select id from brand where name = %s))"""

                # print(query)
                cursor.execute(query2, (rid, brand))
                self._conn.commit()
        finally:
            self._conn.close()
