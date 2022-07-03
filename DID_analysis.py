import numpy as np
import statsmodels.formula.api as smf
import pandas as pd

from data_ploter.data_getter import conn


def DID_analysis():
    t1 = np.array([int(i > 20) for i in range(65)])
    
    print(t1)


def get_data():
    tab = pd.read_sql('select * from GDP', con=conn)

    data_tab = tab.iloc[:, 7:].dropna()

    data_mat = data_tab.values

    print(data_mat.shape)

    # est = smf.ols(formula='v1 ~ t1 + g1 + tg1', data=aa).fit()

    return


if __name__ == '__main__':
    DID_analysis()
