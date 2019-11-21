from json2sql import iJson2Sql
from item import Item
from items_in_category import ItemsInCategory

if __name__ == '__main__':
    # iJson2Sql = Item("../items.json")
    # iJson2Sql.insert_data()
    iJson2Sql = ItemsInCategory("../items.json")
    iJson2Sql.insert_data()