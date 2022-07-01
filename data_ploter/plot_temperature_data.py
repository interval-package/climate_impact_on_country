from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

temperature_path = "./data/temperature.csv"
Nitrous_oxide = "./data/Nitrous_oxide.csv"


def basic_disp():
    tab = pd.read_csv(temperature_path, index_col=None)
    # tab.dropna(inplace=True)
    print(tab)

    data = tab.values

    x_time = [datetime.strptime(str(int(d[0]))+'-'+str(int(d[1])), '%Y-%m') for d in data]

    plt.subplot(1, 2, 1)
    plt.plot(x_time, data[:, 2], label='月平均温度')
    plt.legend(loc="upper right")
    plt.subplot(1, 2, 2)
    plt.plot(x_time, data[:, 3], label='年平均温度')
    plt.plot(x_time, data[:, 4], label='5年平均温度')
    plt.legend(loc="upper right")
    plt.show()
