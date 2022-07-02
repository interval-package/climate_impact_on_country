from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

import data_ploter.plot_temperature_data
import temperature_analysis as t_ana

if __name__ == '__main__':
    # tar = t_ana.temperature_analysis()

    temp = t_ana.temperature_trend()

    temp.arima()

    # print(data)
    pass
