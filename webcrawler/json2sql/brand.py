import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

from json2sql import iJson2Sql
import pymysql
import json
import re


class Brand(iJson2Sql):
    def __init__(self, path):
        self._jsonpath = path
        self._conn = pymysql.connect(host='localhost', user='root', password='rhwk6925', db='tsdb', charset='utf8')
        self.data = self._read_data()

    def _read_data(self):
        with open(self._jsonpath) as json_file:
            data = json.load(json_file)
        return data

    def _get_brand(self):
        brand_set = {}
        for key in self.data.keys():
            brand = self.data[key]["brand"]
            if brand not in brand_set.keys():
                brand_set[brand] = 1
        return brand_set

    def insert_data(self):
        try:
            cursor = self._conn.cursor()
            cnt = 0
            brand_set = self._get_brand()
            for brand in brand_set.keys():
                # query = "insert into brand (id, name) values (" + str(cnt) + ', \'' + brand + '\')'
                query = """insert into brand (id, name) values (%s, %s)"""
                print(query, (cnt, brand))
                cursor.execute(query, (cnt, brand))
                self._conn.commit()
                cnt += 1
        finally:
            self._conn.close()
