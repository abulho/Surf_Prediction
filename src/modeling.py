
import pandas as pd
import numpy as np

def parse_date_to_train_test(filename, train_yrs, test_yrs):
    '''
    input:
    dataframe

    output:
    data belonging to test and train years

    '''
    data = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')

    temp_lst = []
    for year in train_yrs:
        temp_lst.append(data[str(year)])
    df_train = pd.concat(temp_lst, axis=0)

    temp_lst1 = []
    for year in test_yrs:
        temp_lst1.append(data[str(year)])
    df_test = pd.concat(temp_lst1, axis=0)

    return df_train, df_test

if __name__ == "main":
    filename_46005 = 'data_X_y_46005_train.csv'
    filename_46059 = 'data_X_y_46059_train.csv'

    train_yrs = [1995, 2000, 2004, 2006]
    test_yrs = [2007]

    df_train_46005, df_test_46005 = parse_date_to_train_test(filename_46005, train_yrs, test_yrs)
    df_train_46059, df_test_46059 = parse_date_to_train_test(filename_46059, train_yrs, test_yrs)









    '''
    cols = ['YY_x', 'MM_x', 'DD_x', 'hh_x', 'WD_x', 'WSPD_x', 'GST_x', 'WVHT_x',
            'DPD_x', 'APD_x', 'MWD_x', 'BAR_x', 'ATMP_x', 'WTMP_x', 'DEWP_x',
            'VIS_x', 'ID_x', 't_arrive', 'time_delta', 'time_y', 'time_y_hr',
            'YY_y', 'MM_y', 'DD_y', 'hh_y', 'WD_y', 'WSPD_y', 'GST_y', 'WVHT_y',
            'DPD_y', 'APD_y', 'MWD_y', 'BAR_y', 'ATMP_y', 'WTMP_y', 'DEWP_y',
            'VIS_y', 'ID_y'] '''
