import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf


def TimeSeriesPlotter(Data: pd.DataFrame, name):
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


def AcfPlotter(Data: pd.DataFrame):
    for item_idx, item in Data.iteritems():
        # 绘制自相关图
        plot_acf(item, auto_ylims=True).show()
        plt.savefig('data/pics/' + '/AcfPlot_' + str(item_idx) + '.png')
    plt.show()
    pass
