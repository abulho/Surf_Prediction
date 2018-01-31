
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
plt.style.use('ggplot')

def get_train_test(dataframe, cols_to_keep, train_yrs, test_yrs):
    '''
    input:
    dataframe
    list of cosl to drop
    make sure predictor is the last col

    output:
    X --> training
    y --> training
    X --> testing
    y --> testing

    '''
    X_y_data = dataframe
    X_y_interp = X_y_data.interpolate(method='linear', axis=0).bfill()

    dfXy = X_y_interp[cols_to_keep]

    train_lst = []
    for year in train_yrs:
         train_lst.append(dfXy[dfXy['YY_x'] == year])
    train_df = pd.concat(train_lst, axis=0)

    test_lst = []
    for year in test_yrs:
         test_lst.append(dfXy[dfXy['YY_x'] == year])
    test_df = pd.concat(test_lst, axis=0)

    X_train = train_df.values[:,:-1]
    y_train = train_df.values[:,-1:]

    X_test = test_df.values[:,:-1]
    y_test = test_df.values[:,-1:]

    return X_train, X_test, y_train, y_test

def get_Xy_data(filename):
    data = pd.read_csv(filename)
    return data


if __name__ == '__main__':

    filename = '../data/data_X_y_46059_train_w_tide.csv'
    Xy_df = get_Xy_data(filename)

    cols_to_keep = ['YY_x', 'MM_x', 'DD_x', 'hh_x', 'WD_x', 'WSPD_x',
                    'GST_x', 'WVHT_x', 'DPD_x', 'APD_x', 'MWD_x', 'BAR_x', 'ATMP_x',
                    'WTMP_x', 'DEWP_x', 'ID_x', 't_arrive', 'YY_y',
                    'MM_y', 'DD_y', 'hh_y', 'WD_y', 'WSPD_y','GST_y', 'MWD_y', 'BAR_y', 'ATMP_y',
                    'WTMP_y', 'DEWP_y', 'ID_y', 'WaterLevel','WVHT_y']

    train_yrs = [1995, 1996, 1997, 1998, 1999, 2000, 2003, 2004, 2006, 2007]
    test_yrs  = [2008]

    X_train, X_test, y_train, y_test = get_train_test(Xy_df, cols_to_keep, train_yrs, test_yrs)
