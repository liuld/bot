#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import apis.okex.spot_api as spot
from utils import *
from mongo import Mongo
from pymongo import DESCENDING

import time
import json
import logging


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

    last_record = list(cursor.find().sort('time', DESCENDING).limit(1))

    if len(last_record) > 0:
        now = param_time(last_record[0]['time'])
    else:
        now = param_time(get_timestamp())

    while True:
        try:
            result = spotAPI.get_kline(config['symbol'], 60, now)
            for k in result:
                kline_dict = kline_to_dict(k)
                cursor.update_one({'time': kline_dict['time']}, {'$set': kline_dict}, upsert=True)
            if len(result) > 1 and now != result[1][0]:
                now = result[1][0]
        except Exception as e:
            logging.error('get kline error: {}'.format(e))

        time.sleep(5)
