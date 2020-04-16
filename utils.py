#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import datetime


def get_timestamp():
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')


def normal_time(t):
    str_format = '%Y-%m-%d %H:%M:%S'
    utc_time = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8)
    return datetime.datetime.strftime(utc_time, str_format)


def param_time(t):
    str_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    local_time = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=8)
    return datetime.datetime.strftime(local_time, str_format)


def kline_to_dict(kline_list):
    time, open, high, low, close, volume = kline_list[0:]
    return {
        'time': normal_time(time),
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }

