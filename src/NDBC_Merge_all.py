import pandas as pd
import numpy as np
from make_null import *

def merge_all_bouys(filename):

    '''
    input:
    takes in a csv file name

    output:
    merged data frame from all the data extracted from the bouys


    '''
    data_df = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')
    data_df = making_null_values(data_df)

    return data_df

if __name__ == '__main__':
    import os
    import glob
    import time

    file_names = glob.glob('../NDBC_Bouy_Data/data_*.csv')

    all_df_lst = []
    for data_file in file_names:

        print('Merging {}'.format(data_file.split('/')[-1]))

        all_df_lst.append(merge_all_bouys(data_file))

    NDBC_all_data_all_years = pd.concat(all_df_lst, axis = 0)
    NDBC_all_data_all_years.to_csv('../data/NDBC_all_data_all_years.csv')
