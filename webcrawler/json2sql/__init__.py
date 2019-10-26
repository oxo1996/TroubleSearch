if __name__ == '__main__':
    j2s = json2sql("items.json")
    j2s.makeDB("items")