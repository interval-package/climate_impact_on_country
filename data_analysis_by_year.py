from data_ploter.data_loader import conn
import pandas as pd
import numpy as np
import os

forest_path = os.path.join('.', 'data', 'forest.csv')
population_path = os.path.join('.', 'data', 'population.csv')


def get_forest_data():
    forest_tab = pd.read_csv(population_path)
    print(forest_tab)
    forest_tab.to_sql(name='population_tab', con=conn, index=False, if_exists='replace')
    return


def get_yearly_data(is_normalize=False):
    """
    select * from surface_temperature, forest_tab, population_tab
    where surface_temperature.Category = forest_tab.year
    and forest_tab.year = population_tab.year

    :cvar
    """

    tab = pd.read_sql("""
                    select NOAA_National_Climatic_Data_Center as temperature, 
                    area as forest_area, population from surface_temperature, forest_tab, population_tab
                    where surface_temperature.Category = forest_tab.year
                    and forest_tab.year = population_tab.year
                    """
                      , con=conn)

    # print(tab.astype(float))
    tab = tab.astype(float)
    if is_normalize:
        tab = tab.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
        print(tab)
        print(tab.corr())

    return tab


if __name__ == '__main__':
    get_yearly_data()
    pass
