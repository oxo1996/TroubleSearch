import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

from json2sql import iJson2Sql
import pymysql
import json
import re


class Ingredient(iJson2Sql):
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

            for ko_name in self.data.keys():
                table_attr = ["engName", "ewgRank", "koDesc", "engDesc"]
                val_list = []
                for key in table_attr:
                    try:
                        value = self.data[ko_name][key]
                    except KeyError as e:
                        value = None
                    val_list.append(value)

                query = """insert into ingredient (id, ko_name, eng_name, ewg_rank, ko_desc, eng_desc) 
                values(%s, %s, %s, %s, %s, %s)"""
                print(cnt, ko_name)
                cursor.execute(query, (cnt, ko_name, val_list[0], val_list[1], val_list[2], val_list[3]))
                self._conn.commit()
                cnt += 1
        finally:
            self._conn.close()
