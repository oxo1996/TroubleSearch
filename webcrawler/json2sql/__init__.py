import sys

sys.path.append('/django/djangoproject/webcrawler/json2sql')

from json2sql import iJson2Sql
from review import Review
from item import Item
from items_in_brand import ItemsInBrand
from items_in_category import ItemsInCategory
from ingredient import Ingredient
from ingredients_in_item import IngredientsInItem

def execute_query(query : iJson2Sql):
    query.insert_data()

if __name__ == '__main__':
    items_path = "../items.json"
    # r = Review("../items.json")
    # item = Item(items_path)
    # iib = ItemsInBrand(items_path)
    # iic = ItemsInCategory(items_path)
    # query_list = [item, iib, iic]
    # for query in query_list:
    #     execute_query(query)

    # iJson2Sql = Review(items_path)
    # iJson2Sql.insert_data()

    iJson2Sql = IngredientsInItem()
    iJson2Sql.insert_data()

    # iJson2Sql = Ingredient("../ingrDesc.json")
    # iJson2Sql.insert_data()

    #iJson2Sql.insert_data()