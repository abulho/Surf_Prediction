import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil import parser
plt.style.use('ggplot')

def load_train_test_data(filename):
    '''
    input:
    filenme for the train and test data

    output: dataframe
    '''
    data = pd.read_csv(filename, parse_dates=['id_x'])

    return data

def load_tide_data(filename):
    '''
    input:
    filenme for the train and test data

    output: dataframe
    '''
    data = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')

    return data

if __name__ == '__main__':
    df = load_train_test_data('../data/data_X_y_46059_train_012918.csv')
    df['id_test'] = df['time_y_hr'].apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))

    df_tide = load_tide_data('../data/tides.csv')
    df_tide['id'] = df_tide.index

    XX = pd.merge(df, df_tide, how='left', left_on='id_test', right_on='id')
    XX['WaterLevel'] = XX['WaterLevel'].interpolate(method='linear', axis=0).bfill()

    XX.to_csv('../data/data_X_y_46059_train_w_tide.csv')
