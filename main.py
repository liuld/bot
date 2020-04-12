#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import apis.okex.spot_api as spot
from utils import *
from mongo import Mongo

import time
import json
import logging
from pymongo import DESCENDING


log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='log-rest.json', filemode='a', format=log_format, level=logging.INFO)


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    api_key = config['api_key']
    secret_key = config["secret_key"]
    passphrase = config["passphrase"]

    spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)

    mongo = Mongo(
        host=config['mongo_host'],
        port=config['mongo_port'],
        username=config['mongo_username'],
        password=config['mongo_password']
    )

    cursor = mongo.get_db_cursor(config['mongo_db'])[config['mongo_collection']]

    cursor.create_index('time', unique=True)

    last_record = list(mongo.get_last_record(cursor))

    if len(last_record) > 0:
        now = param_time(last_record[0]['time'])
    else:
        now = param_time(get_timestamp())

    while True:
        try:
            result = spotAPI.get_kline(config['symbol'], 60, now)
            for k in result:
                update_or_insert_to_mongodb(cursor, k)
            if now != result[0][0]:
                now = result[0][0]
        except Exception as e:
            logging.error('get kline error: {}'.format(e))

        time.sleep(5)
