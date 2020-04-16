# !/usr/local/bin/python3
# _*_ coding: utf-8 _*_

import pymongo


class Mongo(object):

    def __init__(
            self, host='localhost', port=27017, username=None, password=None):

        if username and password:
            self.conn = pymongo.MongoClient(
                host=host, port=port, username=username, password=password)
        else:
            self.conn = pymongo.MongoClient(host=host, port=port)

    def get_db_cursor(self, db):
        return self.conn[db]

    def get_collection_cursor(self, db, collection):
        return self.conn[db][collection]

    def get_doc(self, db, collection, query={}, filters={}, limit=0, del_id=True):
        if del_id:
            filters['_id'] = 0
        return self.get_collection_cursor(db, collection).find(query, filters).limit(limit)


