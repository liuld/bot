#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import json
import pandas as pd
from mongo import Mongo


def set_dtypes(data_frame):
    data_frame['time'] = pd.to_datetime(data_frame['time'])
    data_frame['open'] = data_frame['open'].astype("float64")
    data_frame['high'] = data_frame['high'].astype("float64")
    data_frame['low'] = data_frame['low'].astype("float64")
    data_frame['close'] = data_frame['close'].astype("float64")
    data_frame['volume'] = data_frame['volume'].astype("float64")
    return data_frame


def re_sample_data(data_frame, rule):
    return data_frame.resample(rule).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
    })


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
    # 查询数据
    data = mongo.get_doc(
        db=config['mongo_db'],
        collection=config['mongo_collection'],
        query={'time': {'$gte': '2020-04-16 16:00:00'}},
        filters={},
        limit=0
    )
    # 处理数据
    df = set_dtypes(pd.DataFrame(list(data)))
    df.set_index('time', inplace=True)

    # 一小时周期合并数据
    one_hours_df = re_sample_data(df, '1H')

    # 四小时周期合并数据
    four_hours_df = re_sample_data(df, '4H')

    print(four_hours_df)
