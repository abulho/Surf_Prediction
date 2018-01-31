import pandas as pd
import numpy as np
from math import pi
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import datetime
from pytz import timezone

import warnings
warnings.filterwarnings('ignore')

def get_train_bouys(filename, buoyID):
    '''
    input: date file filename
           Bouy ID as a list

    output: return data frame with only the buoy selected for train and test

    '''
    data = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')
    data_temp = data[data['ID'] == buoyID]
    data_X = data_temp.interpolate(method ='linear', axis=0).bfill()

    tz = timezone('US/Pacific')
    data_X.index = data_X.index.tz_localize('UTC').tz_convert(tz)
    data_X['TempDate'] = data_X.index
    data_X['YY'] = data_X['TempDate'].apply(lambda x: x.year)
    data_X['MM'] = data_X['TempDate'].apply(lambda x: x.month)
    data_X['DD'] = data_X['TempDate'].apply(lambda x: x.day)
    data_X['hh'] = data_X['TempDate'].apply(lambda x: x.hour)
    data_X.drop(columns='TempDate', inplace = True)

    data_X.index = data_X.index.tz_localize(None)

    return data_X

def get_test_bouys(filename, buoyID):
    '''
    input: date file filename
           Bouy ID as a list

    output: return data frame with only the buoy selected for train and test

    '''
    data = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')
    data_temp = data[data['ID'] == buoyID]
    data_X = data_temp.interpolate(method='linear', axis=0).bfill()
    return data_X

def adding_speed_col(dataframe, distance):
    '''
    input:
    dataframe
    distance from source buoy to target buoy in km

    output:
    wave speed col added to data frame

    # info
    1 m/s = 1.943844 knots
    1 knot = 1.852 km/hr

    '''
    # geting rid of waves with period = 0
    df = dataframe#[dataframe['DPD'] >= 12]
    df['APD'] = df['APD'].apply(lambda x: np.nan if x==0 else x)
    df['APD'] = df['APD'].interpolate(method='linear', axis=0).bfill()

    # speed in km/hr
    speed = ((9.81 * df['APD']) / (2*pi)) * 3.6
    arrive = distance / speed
    df['t_arrive'] = arrive
    return df

def add_time_delta(dataframe):
    dataframe['time_delta'] = dataframe['t_arrive'].apply(lambda x: datetime.timedelta(x/24))
    return dataframe

def add_time_y(dataframe):
    dataframe['time_y'] = dataframe.index + dataframe['time_delta']
    return dataframe

def round_time_y(dataframe):
    dataframe['time_y_hr']  = dataframe['time_y'].apply(lambda dt: datetime.datetime(dt.year,
                                                                                     dt.month,
                                                                                     dt.day,
                                                                                     dt.hour,
                                                                                     0,0))
    return dataframe

def make_hourly_data(dataframe, year):
    '''
    input:
    DataFrame
    year

    output:
    returns a data frame with a constant frequency of points,
    will add points and interpolate to make a full hourly data set for
    the given year.

    '''
    d = pd.date_range(start = '1/1/{} 00:00:00'.format(year),
                      end   = '12/31/{} 23:00:00'.format(year),
                      freq  = '1H')

    df_test = pd.DataFrame(np.nan, index = d, columns = ['dummy'])
    df_test['id'] = df_test.index
    dataframe['id'] = dataframe.index
    df_joined = pd.merge(df_test, dataframe, how='left', left_on='id', right_on='id')

    df_joined.index = df_joined['id']
    df_joined.drop(columns='dummy', inplace=True)
    df_joined = df_joined.interpolate(method='linear', axis=0).bfill()

    return df_joined

def join_all_hourly_data(dataframe, year_list):
    '''
    input:
    takes in a dataframe
    years as list

    output:
    joined data frame with all yeasrs, with houlry intervals filled in
    '''

    df_lst = []

    for year in year_list:
        df_lst.append(make_hourly_data(dataframe, year))

    return pd.concat(df_lst, axis=0)


if __name__ == '__main__':
    filename = '../data/NDBC_all_data_all_years.csv'
    buoyID_train = [46059]
    buoyID_test = [46026]

    print('Processing the data for training and testing')

    # getting the testing and traing data
    #data_train_46005 = get_train_bouys(filename, buoyID_train[0])
    data_train_46059 = get_train_bouys(filename, buoyID_train[0])
    data_labels_46026  = get_train_bouys(filename, buoyID_test[0])

    yr_lst = [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
              2003, 2004, 2006, 2007, 2008]

    data_train_46059_hr = join_all_hourly_data(data_train_46059, yr_lst)
    data_labels_46026_hr  = join_all_hourly_data(data_labels_46026, yr_lst)

    # adding the arrival time column to the data frame
    data_train_46059_t = adding_speed_col(data_train_46059_hr , 650)

    # adding time delta for the data frames
    data_train_46059_t = add_time_delta(data_train_46059_t)

    # adding time to time_delta
    data_train_46059_t = add_time_y(data_train_46059_t)

    #rounding time
    data_train_46059_t = round_time_y(data_train_46059_t)

    #data_X_y_46005 = pd.merge(data_train_46005_t, data_test_46026, left_on='time_y_hr', right_index=True)
    data_X_y_46059 = pd.merge(data_train_46059_t,
                              data_labels_46026_hr,
                              how='left', left_on='time_y_hr', right_on='id')

    #data_X_y_46005.to_csv('data_X_y_46005_train.csv')
    data_X_y_46059.to_csv('data_X_y_46059_train_012918.csv', index=False)

    print('Processing complete')
