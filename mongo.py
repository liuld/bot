#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import pymongo


class Mongo(object):

    def __init__(self, host='localhost', port=27017, username=None, password=None):
        self.client = pymongo.MongoClient(host=host, port=port)
        if username:
            admin = self.client['admin']
            admin.authenticate(username, password)

    def get_db_cursor(self, db):
        return self.client[db]

    def get_doc(self, db, collection):
        return self.get_db_cursor(db)[collection].find().sort('time', pymongo.DESCENDING)

    @staticmethod
    def get_last_record(cursor):
        return cursor.find().sort('time', pymongo.DESCENDING).limit(1)


if __name__ == '__main__':
    import json

    with open('config.json', 'r') as f:
        config = json.load(f)

    mongo = Mongo(
        host=config['mongo_host'],
        port=config['mongo_port'],
        username=config['mongo_username'],
        password=config['mongo_password']
    )

    for i in mongo.get_doc(config['mongo_db'], config['mongo_collection']):
        print(i)

