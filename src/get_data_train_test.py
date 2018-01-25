import pandas as pd
import numpy as np
from make_null import *

def get_data_for_train_test(filename, yearbegin, yearend):

    '''
    input:
    takes in a csv file name

    output:
    data frame will only the dates specified for to choose as test and train]

    '''
    data_df = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')
    data_df = making_null_values(data_df)

    # subsetting the data frames based on year begin and year end
    years = [year for year in range(yearbegin, yearend + 1)]

    temp = []
    for year in years:
        temp.append(data_df[data_df['YY'] == year]) # getting the data frame corresponding to the year
    data_df = pd.concat(temp, axis = 0)

    return data_df

def clean_data_train_test(dataframe):
    '''
    input:
    Dataframe with all the years to consider to for train and testing

    output:
    cleaned X data set for training
    '''

    pass
