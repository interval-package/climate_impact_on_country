import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os.path as path
import sqlite3 as sql

temperature_path = "./data/temperature.csv"
Nitrous_oxide = path.join('.', 'data', 'Nitrous_oxide' + '.csv')
Methane = path.join('.', 'data', 'Methane' + '.csv')
CO2 = path.join('.', 'data', 'CO2' + '.csv')

tab_allowed_names = ['CO2', 'Methane', 'Nitrous_oxide', 'GMSL']

# pre action of connecting database
try:
    data_path = path.join('.', 'data', 'DataBase.db')
    conn = sql.connect(data_path)
except Exception as e:
    print(repr(e))
    data_path = path.join('..', 'data', 'DataBase.db')
    conn = sql.connect(data_path)


def switch_datetime(tar_time):
    tar = tar_time.split('/')
    try:
        res = tar[0] + '/' + tar[1]
    except IndexError as e:
        tar = tar_time.split('-')
        res = tar[0] + '/' + tar[1]
    return res


def get_tab_DatetimeRestruct(name):
    """
    get processed tab of Nitrous_oxide, Methane

    :param name: 'Nitrous_oxide', 'Methane'
    :return: tab of the processed data
    """
    try:
        tar = path.join('.', 'data', name + '.csv')
        tar = pd.read_csv(tar)
    except FileNotFoundError:
        tar = path.join('..', 'data', name + '.csv')
        tar = pd.read_csv(tar)
    tar.dropna(axis=1, inplace=True)
    tar['DateTime'] = tar['DateTime'].apply(switch_datetime)
    return tar


def load_2_DataBase():
    for iter_name in tab_allowed_names:
        temp = get_tab_DatetimeRestruct(iter_name)
        temp.to_sql(iter_name, con=conn, if_exists='replace', index=False)


# load_2_DataBase()
tar = path.join('..', 'data', 'temperature' + '.csv')
tar = pd.read_csv(tar)
# tar.dropna(axis=1, inplace=True)
# tar['DateTime'] = tar['DateTime'].apply(switch_datetime)
tar.dropna(inplace=True)
print(tar)
# tar.to_sql('GMSL', con=conn, if_exists='replace', index=False)

