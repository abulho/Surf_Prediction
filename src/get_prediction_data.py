import pandas as pd
import numpy as np
import requests
from datetime import datetime
from pytz import timezone
from format_train_test import *

def get_prediction_data(buoyID):
    '''
    input:
    takes in the csv file with buoy number and date start of data and date end of data

    ouput:
    buoy data as csv files

    '''

    url = "http://www.ndbc.noaa.gov/data/realtime2/{}.txt".format(buoyID)
    content = requests.get(url)

    with open('../data/data_for_prediction_{}.csv'.format(46059), 'w') as f:
        f.write(content.text)

def clean_prediction_data(filename):
    '''
    input:
    file name

    output:
    clean csv file for use in prediction
    '''
    data = pd.read_csv(filename, sep='\s+', header=[1])
    cols = ['YY', 'MM','DD','hh','mm','WDIR','WSPD','GST','WVHT','DPD','APD','MWD',
            'PRES','ATMP','WTMP','DEWP','VIS','PTDY','TIDE']
    data.columns = cols
    dates_temp = data[['YY','MM','DD','hh']].values
    new_date = [datetime.datetime(*x) for x in dates_temp]
    data['Date'] = new_date

    allcols = data.columns
    pred_test = data[data[allcols] != 'MM']
    cols_to_numerics = ['WDIR', 'WSPD', 'GST', 'WVHT', 'DPD','APD', 'MWD',
                        'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']
    pred_test[cols_to_numerics] = pred_test[cols_to_numerics].apply(pd.to_numeric)

    pred_test = pred_test.interpolate(method='linear', axis=0).bfill()

    data_X = pred_test.copy()
    data_X.index = data_X['Date']

    tz = timezone('US/Pacific')
    data_X.index = data_X.index.tz_localize('UTC').tz_convert(tz)
    data_X['TempDate'] = data_X.index
    data_X['YY'] = data_X['TempDate'].apply(lambda x: x.year)
    data_X['MM'] = data_X['TempDate'].apply(lambda x: x.month)
    data_X['DD'] = data_X['TempDate'].apply(lambda x: x.day)
    data_X['hh'] = data_X['TempDate'].apply(lambda x: x.hour)

    data_X.index = data_X.index.tz_localize(None)

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

if __name__ == '__main__':
    get_prediction_data()
    prediction_df = clean_prediction_data('../data/data_for_prediction.csv')
    prediction_df = adding_speed_col(prediction_df, 650)
    prediction_df = add_time_delta(prediction_df)
    prediction_df = add_time_y(prediction_df)
    prediction_df = round_time_y(prediction_df)

    cols_to_keep = ['YY', 'MM', 'DD', 'hh', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD',
                    'APD', 'PRES', 'ATMP', 'WTMP', 'DEWP', 't_arrive']

    X_real_time_predictions = prediction_df[cols_to_keep].values
