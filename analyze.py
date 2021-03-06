#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import json
import pandas as pd
import talib as ta
import time
import logging


from mongo import Mongo
from wx import WeChat


log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='alert.log', filemode='a', format=log_format, level=logging.INFO)


class ANALYSE(object):

    def __init__(self, data_source):

        self.data_frame = pd.DataFrame(list(data_source))

        pd.set_option('expand_frame_repr', False)
        pd.set_option('display.max_rows', 1000)

        self.data_frame['time'] = pd.to_datetime(self.data_frame['time'])
        self.data_frame['open'] = self.data_frame['open'].astype("float64")
        self.data_frame['high'] = self.data_frame['high'].astype("float64")
        self.data_frame['low'] = self.data_frame['low'].astype("float64")
        self.data_frame['close'] = self.data_frame['close'].astype("float64")
        self.data_frame['volume'] = self.data_frame['volume'].astype("float64")
        self.data_frame.set_index('time', inplace=True)

    def merge_kline(self, rule):
        return self.data_frame.resample(rule).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
        })

    def get_rsi(self, rule):
        data_frame = self.merge_kline(rule)
        rsi_df = pd.DataFrame()
        rsi_df['rsi6'] = ta.RSI(data_frame['close'], timeperiod=6)
        rsi_df['rsi12'] = ta.RSI(data_frame['close'], timeperiod=12)
        rsi_df['rsi24'] = ta.RSI(data_frame['close'], timeperiod=24)
        return rsi_df

    def get_bbands(self, rule):
        data_frame = self.merge_kline(rule)
        bbands_df = pd.DataFrame()
        bbands_df['upperband'], bbands_df['middleband'], bbands_df['lowerband'] = ta.BBANDS(
            data_frame['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        return bbands_df


def alert_message(corp_id, corp_secret, messages):
    try:
        bot = WeChat(corp_id, corp_secret)
        bot.send_msg(messages)
    except Exception as e:
        logging.error("alert_message:", str(e))


if __name__ == '__main__':

    # 加载配置
    with open('config.json', 'r') as f:
        config = json.load(f)

    # 连接mongodb
    mongo = Mongo(
        host=config['mongo_host'],
        port=config['mongo_port'],
        username=config['mongo_username'],
        password=config['mongo_password']
    )

    start_time = config['analyse_start_time']

    decimal = config['analyse_decimal']

    rsi_send_count = boll_send_count = 0

    while True:
        # 查询数据
        data = mongo.get_doc(
            db=config['mongo_db'],
            collection=config['mongo_collection'],
            query={'time': {'$gte': start_time}},
            filters={},
            limit=0
        )

        analyse = ANALYSE(data)

        # 一小时周期数据
        one_hours_data = analyse.merge_kline('1H')

        # 一小时周期boll数据
        one_hours_boll = analyse.get_bbands('1H')

        # 一小时周期rsi数据
        one_hours_rsi = analyse.get_rsi('1H')

        # 判断价格突破boll上/下轨线
        if one_hours_data['close'][-1] >= one_hours_boll['upperband'][-1] or\
                one_hours_data['close'][-1] <= one_hours_boll['lowerband'][-1]:
            if boll_send_count < 3:
                boll_info = 'boll 提醒: 价格突破boll上/下轨线, 当前价格: {} up: {} middle: {}, lower: {}'.format(
                        round(one_hours_data['close'][-1], decimal),
                        round(one_hours_boll['upperband'][-1], decimal),
                        round(one_hours_boll['middleband'][-1], decimal),
                        round(one_hours_boll['lowerband'][-1], decimal)
                )
                logging.info(boll_info)
                alert_message(config['corp_id'], config['corp_secret'], boll_info)
                boll_send_count += 1
        else:
            boll_send_count = 0

        # 判断rsi超买超卖
        if one_hours_rsi['rsi6'][-1] > 93 or one_hours_rsi['rsi6'][-1] < 10:
            if rsi_send_count < 3:
                rsi_info = 'rsi 提醒: rsi6 大于90 或 小于20, 当前rsi值: {}, {}, {}, 价格: {}'.format(
                    one_hours_rsi['rsi6'][-1],
                    one_hours_rsi['rsi12'][-1],
                    one_hours_rsi['rsi24'][-1],
                    one_hours_data['close'][-1]
                )
                logging.info(rsi_info)
                alert_message(config['corp_id'], config['corp_secret'], rsi_info)
                rsi_send_count += 1
        else:
            send_count = 0

        time.sleep(15)
