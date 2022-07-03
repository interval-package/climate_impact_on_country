import matplotlib.pyplot as plt
from sklearn.datasets import make_regression

from temperature_analysis import *

from data_ploter.data_getter import *

from sklearn.neural_network import MLPRegressor

import statsmodels.api as stm


def ADFGetter(Data, max_lags=5):
    # Data.dropna(axis=0, inplace=True)
    adfResult = stm.tsa.stattools.adfuller(Data, max_lags)
    i = 0
    while adfResult[1] > 0.002:
        i += 1
        Data = np.diff(Data)
        adfResult = stm.tsa.stattools.adfuller(Data, max_lags)
    print(i)

    output = pd.DataFrame(index=['Test Statistic Value', "p-value", "Lags Used", "Number of Observations Used",
                                 "Critical Value(1%)", "Critical Value(5%)", "Critical Value(10%)"],
                          columns=['value'])
    output['value']['Test Statistic Value'] = adfResult[0]
    output['value']['p-value'] = adfResult[1]
    output['value']['Lags Used'] = adfResult[2]
    output['value']['Number of Observations Used'] = adfResult[3]
    output['value']['Critical Value(1%)'] = adfResult[4]['1%']
    output['value']['Critical Value(5%)'] = adfResult[4]['5%']
    output['value']['Critical Value(10%)'] = adfResult[4]['10%']
    return output


class multi_env_factor_analysis:
    """
    这里我们要做的是，将不同的环境因素作为诱因，判断是否是这些因素的变化使得气候发生了变化。\n
    选用bp神经网络模型，将前一天的温度与相关的排放指标作为输入参数，去预测接下来的发生情况。
    """

    def __init__(self):
        self.tab = get_connected_data()
        # self.tab.rename(columns={'Monthly_Data': 'CO2', 'Trend': 'CH4'}, inplace=True)

        # data = self.tab.values[:, 1:-2]
        # print(data)
        pass

    def calc_corr(self, is_save=False):
        res = self.tab.corr('spearman')
        print(res)
        if is_save:
            res.to_csv("./corr.csv")

    def disp_raw(self):
        data = self.tab.values

        plt.subplot(2, 2, 1)
        plt.plot(data[:, 1], label='二氧化碳浓度')
        plt.legend()
        plt.subplot(2, 2, 2)
        plt.plot(data[:, 2], label='一氧化二氮浓度')
        plt.legend()
        plt.subplot(2, 2, 3)
        plt.plot(data[:, 3], label='气温')
        plt.legend()
        plt.subplot(2, 2, 4)
        plt.plot(data[:, 4], label='气温')
        plt.legend()

        plt.show()

    def adf_analysis(self):
        data = self.tab.values
        for col, i in zip(data[:, 1:-1].transpose(), range(3)):
            temp = ADFGetter(col)
            temp.to_csv('./{}.csv'.format(str(i)))

    def bp_fit(self):
        _data = self.tab.values
        gap = int(len(_data) / 2)

        _data_tr = _data[:gap]
        _data_te = _data[gap:]

        data_tr = _data_tr[:, 1:-2]
        data_tr_res = _data_tr[:, -1]
        # data_te = data[gap:]

        data_te = _data_te[:, 1:-2]
        data_te_res = _data_te[:, -1]

        model = MLPRegressor(hidden_layer_sizes=(100,),
                             activation='logistic',
                             random_state=1, learning_rate_init=0.1)  # BP神经网络回归模型
        model.fit(data_tr, data_tr_res)  # 训练模型
        pre = model.predict(data_tr)  # 模型预测
        plt.plot(data_tr_res, label='真实数据')
        plt.plot(pre, label='预测数据')
        plt.legend()
        plt.show()

    def arima(self):
        # 利用ARIMA模型进行预测
        tab = self.tab[['CO2_res', 'SF4_res', 'Methane_res']].dropna()
        for col in tab:
            data = self.tab[col].values
            print(data)
            model = ARIMA(data, order=(5, 1, 5)).fit()  # 传入参数，构建并拟合模型
            predict_data = model.predict(1, len(data)+10)  # 预测数据
            forecast_data = model.forecast(30)
            f = plt.figure(facecolor='white')
            plt.subplot(1, 2, 1)
            plt.title(col)
            plt.plot(data, label='训练数据')
            plt.plot(predict_data, label='预测数据')
            plt.legend()
            plt.subplot(1, 2, 2)
            plt.plot(forecast_data, label='未来预测')
            plt.legend()
            plt.show()


if __name__ == '__main__':
    obj = multi_env_factor_analysis()
    print(obj.tab)
    obj.arima()

    # obj.calc_corr(False)
    # obj.adf_analysis()
    # obj.disp_raw()
    # obj.bp_fit()

    pass
