from temperature_analysis import *

from data_ploter.data_getter import *


class multi_env_factor_analysis:
    """
    这里我们要做的是，将不同的环境因素作为诱因，判断是否是这些因素的变化使得气候发生了变化。\n
    选用bp神经网络模型，将前一天的温度与相关的排放指标作为输入参数，去预测接下来的发生情况。
    """

    def __init__(self):
        self.tab = get_connected_data()
        pass


if __name__ == '__main__':

    pass
