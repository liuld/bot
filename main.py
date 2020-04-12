#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


# from mongo import Mongo
import apis.okex.spot_api as spot
import json
import logging
import datetime


log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='log-rest.json', filemode='a', format=log_format, level=logging.INFO)

def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


time = get_timestamp()

if __name__ == '__main__':
    api_key = "d3bf2e61-a028-468b-8aab-c7f30c40d114"
    secret_key = "EF5705BA5920BE09D84E06058D95BD69"
    passphrase = ""

    spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
    result = spotAPI.get_kline('XRP-USDT', 60)
    print(result)
    # mongo = Mongo(host='192.168.10.20', port=27017)
    # collections = mongo.client.admin.get_collection('system.version')
    # print(dir(collections))

