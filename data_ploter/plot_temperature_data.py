from datetime import datetime

from data_analysis_by_year import get_yearly_data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

temperature_path = "../data/temperature.csv"
Nitrous_oxide = "../data/Nitrous_oxide.csv"


def basic_disp():
    tab = pd.read_csv(temperature_path, index_col=None)
    # tab.dropna(inplace=True)
    print(tab)

    data = tab.values

    x_time = [datetime.strptime(str(int(d[0])) + '-' + str(int(d[1])), '%Y-%m') for d in data]

    plt.subplot(1, 2, 1)
    plt.plot(x_time, data[:, 2], label='月平均温度')
    plt.legend(loc="upper right")
    plt.subplot(1, 2, 2)
    plt.plot(x_time, data[:, 3], label='年平均温度')
    plt.plot(x_time, data[:, 4], label='5年平均温度')
    plt.legend(loc="upper right")
    plt.show()


def get_forcast_data():
    tab = pd.read_csv('../data/temp_avg_year.csv')
    print(tab)
    return tab


def yearly_connect():
    data = get_yearly_data()
    print(data)
    return


if __name__ == '__main__':
    # yearly_connect()
    tab = get_forcast_data()

    cur = tab[0:141]
    future = tab[139:]

    plt.plot(cur['year'], cur['temp'], label='history_data')
    plt.plot(future['year'], future['temp'], label='future_predict')
    plt.legend()
    plt.show()

    pass
