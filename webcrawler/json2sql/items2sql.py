class json2sql:
    def __init__(self, path):
        self.readjson = path
        self.conn = pymysql.connect(host='localhost', user='root', password='rhwk6925', charset='utf8mb4')
    
    def makeDB(self, name):
        try:
            with self.conn.cursor() as cursor:
                sql = 'CREATE DATABASE ' + name
                cursor.execute(sql)
            self.conn.commit()
        finally:
            self.conn.close()

    def makeTable(self, name):
        try:
            with self.conn.cursor() as cursor: