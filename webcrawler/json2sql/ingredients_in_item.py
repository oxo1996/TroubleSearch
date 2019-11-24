import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

from json2sql import iJson2Sql
import pymysql
import json
from pymysql.err import IntegrityError


class IngredientsInItem(iJson2Sql):
    def __init__(self):
        self._conn = pymysql.connect(host='localhost', user='root', password='rhwk6925', db='tsdb', charset='utf8')
        self.items = self._read_data("../items.json")
        self.ingr_ko2eng = self._read_data("../ingrKo2Eng.json")

    @staticmethod
    def _read_data(path):
        with open(path) as json_file:
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
            for pname in self.items.keys():
                ko_name_ingr_list = self.items[pname]["ingredients"]
                item_id = self._find_attr_in_table("item", "id", "name", pname)
                for ko_name in ko_name_ingr_list:
                    # print(ingr)
                    try:
                        eng_name = self.ingr_ko2eng[ko_name]
                    except KeyError as e:
                        print("not exist ingredient information")
                        continue

                    try:
                        ingr_id = self._find_attr_in_table("ingredient", "id", "eng_name", eng_name)
                        cursor = self._conn.cursor()
                        query = """insert into ingredients_in_item (item_id, ingredient_id) values (%s, %s)"""
                        cursor.execute(query, (item_id, ingr_id))
                        self._conn.commit()
                        print(ko_name + " insert success")
                    except IntegrityError as e:
                        print(eng_name, e)
                        continue
        finally:
            self._conn.close()

        print("finish")
