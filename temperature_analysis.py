import logging
from datetime import datetime, timedelta
from sqlite3 import DatabaseError

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_ploter.data_getter import conn as tar_conn

from data_ploter.plot_temperature_data import *

from statsmodels.tsa.arima.model import ARIMA

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def draw_acf_pacf(data, lags):
    f = plt.figure(facecolor='white')
    ax1 = f.add_subplot(211)
    plot_acf(data, ax=ax1, lags=lags)
    ax2 = f.add_subplot(212)
    plot_pacf(data, ax=ax2, lags=lags)
    plt.subplots_adjust(hspace=0.5)
    plt.show()


class temperature_analysis:
    def __init__(self):
        self.detail_tab = pd.read_csv(temperature_path, index_col=None)
        temp_data = self.detail_tab.values
        self.raw_x_time = [datetime.strptime(str(int(d[0])) + '-' + str(int(d[1])), '%Y-%m')
                           for d in temp_data]
        pass

    def get_x_ticks(self, is_raw=True):
        if is_raw:
            temp_data = self.detail_tab.values
        else:
            temp_data = (self.detail_tab.dropna()).values
        x_time = [datetime.strptime(str(int(d[0])) + '-' + str(int(d[1])), '%Y-%m')
                  for d in temp_data]
        return x_time

    def get_x_ticks_predict(self, nums):
        start = max(self.get_x_ticks(is_raw=False))
        res = [start + timedelta(30 * i) for i in range(nums)]
        return res

    def get_monthly(self):
        temp_data = self.detail_tab.dropna().values
        res = temp_data[:, 2]
        return res

    @staticmethod
    def draw_acf_pacf(data, lags):
        f = plt.figure(facecolor='white')
        ax1 = f.add_subplot(211)
        plot_acf(data, ax=ax1, lags=lags)
        ax2 = f.add_subplot(212)
        plot_pacf(data, ax=ax2, lags=lags)
        plt.subplots_adjust(hspace=0.5)
        plt.show()

    def acf_pacf(self):
        """
        分析数据确定acf与pacf的值，确定为 p = 12, q = 24

        :return:
        """
        monthly_avg = self.get_monthly()
        monthly_avg = np.diff(monthly_avg, 1)
        # print(monthly_avg)
        # plt.plot(monthly_avg)
        self.draw_acf_pacf(monthly_avg, lags=35)
        pass

    def arima_analysis(self, forcast_nums=100):

        data = np.array(self.get_monthly())

        print(data)

        sub_data = data[0:1000]

        # 利用ARIMA模型进行预测
        model = ARIMA(data, order=(5, 1, 5)).fit()  # 传入参数，构建并拟合模型
        predict_data = model.predict(0, len(data) - 1)  # 预测数据
        forecast = model.forecast(forcast_nums)  # 预测未来数据

        # 绘制原数据和预测数据对比图
        f = plt.figure(facecolor='white')
        plt.subplot(1, 2, 1)
        plt.plot(self.get_x_ticks(is_raw=False), data, label='训练数据')
        plt.plot(self.get_x_ticks(is_raw=False), predict_data, label='预测数据')
        plt.subplot(1, 2, 2)
        plt.plot(self.get_x_ticks_predict(forcast_nums), forecast)
        plt.legend()
        plt.show()
        pass


class temperature_trend:
    data_centres = [
        'Met_Office_Hadley_Centre/Climatic_Research_Unit', 'Japanese_Meteorological_Agency',
        'NASA_Goddard_Institute_for_Space_Studies', 'NOAA_National_Climatic_Data_Center'
    ]
    data_dict = {}

    def __init__(self):
        try:
            ques = """
            select * from surface_temperature
            """
            tab = pd.read_sql(sql=ques, con=tar_conn)
        except DatabaseError:
            tab = None
        except Exception as e:
            logging.warning(repr(e))
            tab = None
        self.tab = tab
        pass

    def read_data(self, centre=None):
        """
        get the trend data from different centre, centre should be in the member list 'data_centres'

        :param centre:
        :return:
        """

        if centre is None:
            centre = self.data_centres[0]

        try:
            ques = """
            select Category, {} from surface_temperature
            """.format(centre)
            tab = pd.read_sql(sql=ques, con=tar_conn)
        except DatabaseError:
            tab = None
        except Exception as e:
            logging.warning(repr(e))
            tab = None
        return tab

    def process_data(self):
        tab = self.tab
        tab = tab.dropna(axis=0)
        data = tab[self.data_centres].values
        pos = np.where(data == 'null')[0]
        data = np.delete(data, pos, axis=0).astype(float)
        return data

    def disp_temp(self):
        data = self.process_data()
        for name, i in zip(self.data_centres, range(data.shape[1])):
            plt.plot(data[:, i], label=name)
        plt.legend()
        plt.show()

    def pacf(self):
        # 先取平均值，作为目标
        data = np.apply_along_axis(func1d=np.mean, axis=1, arr=self.process_data())
        draw_acf_pacf(data, lags=25)
        # print(data)

        # p = 10, q = 4

    def arima(self):
        # 利用ARIMA模型进行预测
        data = np.apply_along_axis(func1d=np.mean, axis=1, arr=self.process_data())
        model = ARIMA(data, order=(10, 1, 4)).fit()  # 传入参数，构建并拟合模型
        predict_data = model.predict(1, len(data))  # 预测数据
        forcast_data = model.forecast(10)
        f = plt.figure(facecolor='white')
        plt.subplot(1, 2, 1)
        plt.plot(data, label='训练数据')
        plt.plot(predict_data, label='预测数据')
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(forcast_data, label='未来预测')
        plt.legend()
        plt.show()
