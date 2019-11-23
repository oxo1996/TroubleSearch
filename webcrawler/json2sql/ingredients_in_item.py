import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

from json2sql import iJson2Sql
import pymysql
import json
from pymysql.err import IntegrityError


class IngredientsInItem(iJson2Sql):
    def __init__(self, path):
        self._jsonpath = path
        self._conn = pymysql.connect(host='localhost', user='root', password='rhwk6925', db='tsdb', charset='utf8')
        self.data = self._read_data()

    def _read_data(self):
        with open(self._jsonpath) as json_file:
            data = json.load(json_file)
        return data

    def _find_attr_in_table(self, table, select_col, where_col, value):
        cursor = self._conn.cursor()
        query = "select " + select_col + " from " + table + " where " + where_col + " = %s"
        cursor.execute(query, value)
        id = cursor.fetchone()
        return id

    def insert_data(self):
        try:
            for pname in self.data.keys():
                ingr_list = self.data[pname]["ingredients"]
                item_id = self._find_attr_in_table("item", "id", "name", pname)
                for ingr in ingr_list:
                    # print(ingr)
                    try:
                        ingr_id = self._find_attr_in_table("ingredient", "id", "ko_name", ingr)
                        cursor = self._conn.cursor()
                        query = """insert into ingredients_in_item (item_id, ingredient_id) values (%s, %s)"""
                        cursor.execute(query, (item_id, ingr_id))
                        self._conn.commit()
                    except IntegrityError as e:
                        print(ingr, e)
                        continue
        finally:
            self._conn.close()

        print("finish")
