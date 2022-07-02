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


if __name__ == '__main__':
    # # load_2_DataBase()
    # tar = path.join('..', 'data', 'sea_temperature' + '.csv')
    # tar = pd.read_csv(tar)
    # # tar.dropna(axis=1, inplace=True)
    # # tar['DateTime'] = tar['DateTime'].apply(switch_datetime)
    # tar.dropna(inplace=True)
    # print(tar)
    # # tar.to_sql('GMSL', con=conn, if_exists='replace', index=False)
    # temp_tab = tar[['m_avg', 'y_avg']]
    # temp_tab['DateTime'] = tar.apply(func=lambda x: str(int(x['year'])) + '/' + str(int(x['month'])), axis=1)
    # temp_tab.to_sql(name='sea_temperature', con=conn, index=False, if_exists='replace')

    # load_2_DataBase()
    tar = path.join('..', 'data', 'SF4' + '.csv')
    tar = pd.read_csv(tar)
    tar.dropna(inplace=True)
    tar['DateTime'] = tar['DateTime'].apply(switch_datetime)
    tar.rename(columns={'Trend': 'SF4_res'}, inplace=True)
    print(tar)


    # print(tar.rename({'Monthly': 'res_t'}, inplace=True))
    tar[['DateTime', 'SF4_res']].to_sql(name='SF4', con=conn, index=False)
