import pandas as pd
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import datetime

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
    data_X = data_temp.interpolate(method='linear', axis=0).bfill()
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
    df = dataframe[dataframe['DPD'] >= 12]

    # speed in km/hr
    speed = ((9.81 * df['DPD']) / (2*pi)) * 3.6
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
    df_joined = df_joined.interpolate(method='linear', axis=0).bfill()

    return df_joined

if __name__ == '__main__':
    filename = '../data/train_X_y.csv'
    buoyID_train = [46005, 46059]
    buoyID_test = [46026]

    print('Processing the data for training and testing')

    # getting the testing and traing data
    data_train_46005 = get_train_bouys(filename, buoyID_train[0])
    data_train_46059 = get_train_bouys(filename, buoyID_train[1])
    data_test_46026  = get_train_bouys(filename, buoyID_test)

    # adding the arrival time column to the data frame
    data_train_46005_t = adding_speed_col(data_train_46005,1141)
    data_train_46059_t = adding_speed_col(data_train_46059,620)

    # adding time delta for the data frames
    data_train_46005_t = add_time_delta(data_train_46005_t)
    data_train_46059_t = add_time_delta(data_train_46059_t)

    # adding time to time_delta
    data_train_46005_t = add_time_y(data_train_46005_t)
    data_train_46059_t = add_time_y(data_train_46059_t)

    #rounding time
    data_train_46005_t = round_time_y(data_train_46005_t)
    data_train_46059_t = round_time_y(data_train_46059_t)

    data_X_y_46005 = pd.merge(data_train_46005_t, data_test_46026, left_on='time_y_hr', right_index=True)
    data_X_y_46059 = pd.merge(data_train_46059_t, data_test_46026, left_on='time_y_hr', right_index=True)

    data_X_y_46005.to_csv('data_X_y_46005_train.csv')
    data_X_y_46059.to_csv('data_X_y_46059_train.csv')

    print('Processing complete')
