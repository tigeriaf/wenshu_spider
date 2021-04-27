from pymongo import MongoClient


settings = {
    # "ip": '64.115.5.33',  # ip
    "ip": '127.0.0.1',  # ip
    "port": 27017,  # 端口
    "db_name": "wenchuwang_result",
}


class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
            # self.conn.admin.authenticate(settings["username"], settings["password"])
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db["wsw_set"]

    def db_list(self):
        db_list = self.conn.list_database_names()

        for db_name in db_list:
            print(db_name)

    def set_list(self):
        collist = self.db.list_collection_names()
        for set_name in collist:
            print(set_name)

    def insert(self, dic):
        print("inser...")
        self.my_set.insert_one(dic)

    def update(self, dic, newdic):
        print("update...")
        self.my_set.update(dic, newdic)

    def delete(self, dic):
        print("delete...")
        self.my_set.remove(dic)

    def dbfind(self, dic):
        print("find...")
        data = self.my_set.find(dic)
        for result in data:
            if result["s5"]:
                return True
        return False


