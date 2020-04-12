#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import apis.okex.spot_api as spot
from utils import *
from mongo import Mongo

import time
import logging


log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='log-rest.json', filemode='a', format=log_format, level=logging.INFO)


if __name__ == '__main__':
    api_key = "d3bf2e61-a028-468b-8aab-c7f30c40d114"
    secret_key = "EF5705BA5920BE09D84E06058D95BD69"
    passphrase = ""

    spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)

    mongo = Mongo(host='192.168.10.20', port=27017)

    cursor = mongo.get_db_cursor('symbol')['btc']
    # cursor.create_index('time', unique=True)

    now = param_time(get_timestamp())

    while True:
        try:
            result = spotAPI.get_kline('BTC-USDT', 60, now)
            for k in result:
                update_or_insert_to_mongodb(cursor, k)
            if now != result[0][0]:
                now = result[0][0]
        except Exception as e:
            logging.error('get kline error: {}'.format(e))

        time.sleep(5)
