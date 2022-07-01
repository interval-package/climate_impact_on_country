from sqlite3 import OperationalError

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os.path as path
import sqlite3 as sql

# pre action of connecting database
try:
    data_path = path.join('.', 'data', 'DataBase.db')
    conn = sql.connect(data_path)
except OperationalError as e:
    data_path = path.join('..', 'data', 'DataBase.db')
    conn = sql.connect(data_path)


able_factors = []

country_names = ['科威特', '阿拉伯埃及共和国', '阿尔及利亚', '伊朗伊斯兰共和国',
                 '土耳其', '奥地利', '匈牙利', '瑞士', '卢森堡', '乌干达', '泰国', '马来西亚', '菲律宾',
                 '新加坡', '墨西哥', '美国', '加拿大', '日本', '英国', '法国', ]

country_types = ['荒漠国', '内陆国', '热带国', '海洋国', ]


class county_data:
    def __init__(self):
        pass
