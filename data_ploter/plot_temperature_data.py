import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

temperature_path = "./data/temperature.csv"
Nitrous_oxide = "./data/Nitrous_oxide.csv"


def disp():
    tab = pd.read_csv(temperature_path, index_col=None)
    tab.dropna(inplace=True)
    data = tab.values
    print(data[:, 2])
    plt.plot(data[:, 2])
    plt.plot(data[:, 3])
    plt.plot(data[:, 4])
    plt.show()

