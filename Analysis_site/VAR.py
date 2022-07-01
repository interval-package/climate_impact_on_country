import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as stm
import statsmodels.stats.diagnostic as dia


def GetClasses():
    Data = pd.read_excel("data/info/USA.xlsx")
    classNames = pd.value_counts(Data['Product Group']).index.array
    return Data, classNames


def ReadTariffData(Data: pd.DataFrame, Name: str):
    Data = Data[Data['Product Group'] == Name][:]
    # 要加上inplace=True 才能在原数据上修改
    Data.rename(index=Data["Indicator"], inplace=True)
    DropItem = ['Partner Name', 'Reporter Name', 'Trade Flow',
                'Product Group', 'Indicator',
                '1993', '1994']
    Data.drop(DropItem, axis=1, inplace=True)
    Data = Data.stack().unstack(0)
    Data = Data.dropna(axis=0, how='any')
    DropItem = ['AHS AVE Tariff Lines Share (%)']
    Data.drop(DropItem, axis=1, inplace=True)
    return Data


def DataProcesser(Data: pd.DataFrame):
    for name in Data.columns:
        if name.find("%") < 0:
            Data[name] = Data[name].apply(np.log)
    return Data


def TimeSeriesPloter(Data: pd.DataFrame, name):
    idx = 1
    plt.figure("trend", figsize=(16, 16))
    for item_idx, item in Data.iteritems():
        # print(item_idx,'\n',item,'\n',type(item))
        plt.subplot(2, 3, idx)
        item.plot()
        plt.title(item_idx)
        idx += 1
    plt.savefig('data/pics/' + '/timeseries' + name + '.png')
    plt.show()
    pass


def AcfPloter(Data: pd.DataFrame):
    for item_idx, item in Data.iteritems():
        # 绘制自相关图
        plot_acf(item, auto_ylims=True).show()
        plt.savefig('data/pics/' + '/AcfPlot_' + str(item_idx) + '.png')
    plt.show()
    pass


def PacfPloter(Data: pd.DataFrame):
    for item_idx, item in Data.iteritems():
        # 绘制偏自相关图
        plot_pacf(item, lags=10).show()
        plt.savefig('data/pics/' + '/PacfPlot_' + str(item_idx) + '.png')
    plt.show()
    pass


def ADFGetter(Data: pd.DataFrame, maxlags=5):
    Data.dropna(axis=0, inplace=True)
    adfResult = stm.tsa.stattools.adfuller(Data, maxlags)
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


def PackedADFGetter(Data: pd.DataFrame):
    result = []
    for item_idx, item in Data.iteritems():
        out = ADFGetter(pd.DataFrame(item))
        result.append(out)
    return Data, result


def CointDivide(Data: pd.DataFrame):
    Data.dropna(axis=0, inplace=True)
    result = []
    for item_idx, item in Data.iteritems():
        for item_idx_inner, item_inner in Data.iteritems():
            if item_idx_inner != item_idx:
                try:
                    out = stm.tsa.stattools.coint(item, item_inner)
                    # print(out)
                    result.append(out)
                except Warning:
                    Data.drop([item_idx, item_idx_inner], axis=1)
    return Data, result


def MAXVARFitter(Data: pd.DataFrame, varLagNum=5):
    # 建立对象，dataframe就是前面的data，varLagNum就是你自己定的滞后阶数
    orgMod = stm.tsa.VARMAX(Data, order=(varLagNum, 0), trend='n', exog=None)
    # 估计：就是模型
    fitMod = orgMod.fit(maxiter=1000, disp=False)
    # 打印统计结果
    # print(fitMod.summary())
    # 获得模型残差
    resid = fitMod.resid
    return fitMod, resid


def VARFitter(Data: pd.DataFrame, lags=3):
    VARModel = stm.tsa.VAR(Data)
    result = VARModel.fit(lags)
    # print(result.summary())
    return VARModel, result


def FevdPic(FitMod, Name: str, file):
    fevd = FitMod.fevd(10)
    # 打印出方差分解的结果
    print(fevd.summary(), file=file)
    # 画图
    fevd.plot(figsize=(12, 16))
    plt.savefig('data/pics/' + '/FevdPic_' + Name + '.png')
    plt.show()
    pass


def CUSUM(resid):
    # 原假设：无漂移（平稳），备择假设：有漂移（不平稳）
    # het_breuschpagan()
    # diagnostic
    result = dia.breaks_cusumolsresid(resid)
    return result


def ImpulsePic(fitMod, terms=3):
    # orthogonalized=True，代表采用乔里斯基正交
    ax = fitMod.impulse_responses(terms, orthogonalized=True).plot(figsize=(12, 16))
    plt.savefig('data/pics/' + '/ImpulsePic' + '.png')
    plt.show()
    return None


def main():
    plotFlag = False

    Data_base, className = GetClasses()

    # 不想再进行分析的数据，进行跳过，这里可以是空的
    usedName = ['All Products', 'Mach and Elec', 'Vegetable',
                'Transportation', 'Textiles and Clothing', 'Stone and Glass',
                'Plastic or Rubber', 'Miscellaneous', 'Minerals', 'Metals',
                'Hides and Skins', 'Capital goods', 'Fuels', 'Footwear', 'Food Products',
                'Chemicals', 'Animal', 'Raw materials', 'Intermediate goods',
                'Consumer goods', 'Wood']

    for name in className:
        print(name)
        if name.strip() in usedName:
            continue
        input("any to init:")
        Data = ReadTariffData(Data_base, name)
        Data = DataProcesser(Data)
        name = name.strip()
        if plotFlag:
            try:
                file = open('data/' + name + '/' + name + '.txt', mode='w')
            except FileNotFoundError:
                file = open('data/' + name + '.txt', mode='w')
        else:
            file = None
        if plotFlag:
            TimeSeriesPloter(Data=Data, name=name)
            input("any to start next: ")
            AcfPloter(Data=Data)
            input("any to start next: ")
            PacfPloter(Data=Data)

        info = PackedADFGetter(Data)[1]
        info = CointDivide(Data)[1]

        lags = 3
        obj, fitMod_var = VARFitter(Data, lags)
        print(fitMod_var.summary(), file=file)
        if plotFlag:
            FevdPic(fitMod_var, name, file=file)

        input("anything to start maxvar: ")

        fitMod_maxvar, resid = MAXVARFitter(Data, lags)
        print(fitMod_maxvar.summary(), file=file)
        input("any to start next: ")
        if plotFlag:
            ImpulsePic(fitMod_maxvar)
        input("any to start next: ")
        try:
            if plotFlag:
                CUSUM(resid)
        except:
            warnings.warn("CUSUM fail")
        if file:
            file.close()
        onceMode = input("\nnext item or not? input num>0 to next:")
        if int(onceMode) > 0:
            continue
        else:
            break
    pass


def afterMain():
    pass


if __name__ == '__main__':
    main()