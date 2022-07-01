from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

import data_ploter.data_getter

from data_ploter.plot_temperature_data import *

from statsmodels.tsa.arima.model import ARIMA

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class temperature_analysis:
    def __init__(self):
        self.tab = pd.read_csv(temperature_path, index_col=None)
        temp_data = self.tab.values
        self.raw_x_time = [datetime.strptime(str(int(d[0])) + '-' + str(int(d[1])), '%Y-%m')
                           for d in temp_data]
        pass

    def get_x_ticks(self, is_raw=True):
        if is_raw:
            temp_data = self.tab.values
        else:
            temp_data = (self.tab.dropna()).values
        x_time = [datetime.strptime(str(int(d[0])) + '-' + str(int(d[1])), '%Y-%m')
                  for d in temp_data]
        return x_time

    def get_x_ticks_predict(self, nums):
        start = max(self.get_x_ticks(is_raw=False))
        res = [start + timedelta(30 * i) for i in range(nums)]
        return res

    def get_monthly(self):
        temp_data = self.tab.dropna().values
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
        分析数据确定acf与pacf的值，确定为 p = 186, q = 125

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
        predict_data = model.predict(0, len(data)-1)  # 预测数据
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
