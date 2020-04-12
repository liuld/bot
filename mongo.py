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
