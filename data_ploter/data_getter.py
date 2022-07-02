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

tab_allowed_names = ['CO2', 'Methane', 'Nitrous_oxide', 'GMSL']


def get_data_from_base(name):
    ques = "select * from " + name
    df = pd.read_sql(ques, conn)
    return df


def get_connected_data():
    ques = """
        select CO2.DateTime, Monthly_Data, Trend,  Reconstructed_GMSL, m_avg, y_avg 
        from CO2, Methane, GMSL, temperature
        where 
        CO2.DateTime = Methane.DateTime and
        Methane.DateTime = GMSL.DateTime and
        temperature.DateTime = CO2.DateTime
    """
    df = pd.read_sql(ques, conn)
    print(df)
    return

