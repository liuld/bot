#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import pymongo


class Mongo(object):

    def __init__(self, host='localhost', port=27017):
        self.client = pymongo.MongoClient(host=host, port=port)

    def get_db_cursor(self, db):
        return self.client[db]
