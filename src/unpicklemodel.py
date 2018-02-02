import pickle
from datetime import date, datetime, timedelta
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def unpickle_model(pickle_model_name):
    with open(pickle_model_name, 'rb') as f:
        model = pickle.load(f)
    return model

def return_real_time_prediction(pickle_model_name):

    model = unpickle_model(pickle_model_name)

    buoyID = 46059
    get_prediction_data(buoyID)
    prediction_df = clean_prediction_data('../data/data_for_prediction_{}.csv'.format(buoyID))
    prediction_df = adding_speed_col(prediction_df, 650)
    prediction_df = add_time_delta(prediction_df)
    prediction_df = add_time_y(prediction_df)
    prediction_df = round_time_y(prediction_df)
    prediction_df.to_csv('../data/prediction_df.csv')

    prediction_df['ID'] = 46059

    cols_to_keep = ['YY', 'MM', 'DD', 'hh', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD',
                'APD', 'PRES', 'ATMP', 'WTMP', 'DEWP', 'ID', 't_arrive']

    X_real_time_predictions = prediction_df[cols_to_keep].values

    # real time predictions at nearshore from the offshore conditions at offshore buoy 46059
    y_hat_realtime = model.predict(X_real_time_predictions)

    # adding the model predicted data to the dataframe
    prediction_df['y_hat'] = y_hat_realtime

    # making the prediction df index to 'time_y_hr'
    prediction_df.index = prediction_df['time_y_hr']

    # resampling the the data frame by the hour
    yy_resample = prediction_df.resample('H').mean()

    # adding an hour col to the df to parse it by 6am, 12pm and 6pm
    yy_resample['date_fig'] = yy_resample.index
    yy_resample['hr_fig'] = yy_resample['date_fig'].apply(lambda x: x.hour)
    bar_yy = yy_resample[(yy_resample['hr_fig']==6) | (yy_resample['hr_fig']==12) | (yy_resample['hr_fig']==18)]

    # interpolating to fill in the missing gaps
    bar_yy = bar_yy.interpolate(method='linear', axis=0).bfill()

    return bar_yy


def make_plot_times():
    dt = date.today()
    dt_midnight = datetime.combine(dt, datetime.min.time())
    time_start = dt_midnight + timedelta(hours = 24)
    time_end = dt_midnight + timedelta(hours = 168)

    return time_start, time_end


def make_dash_board():

    time_start, time_end = make_plot_times()
    bar_yy = return_real_time_prediction('gbr_2.pkl')

    myFmt = mdates.DateFormatter('%H:%S')

    fig, ax = plt.subplots(figsize=(18,6))
    ax.bar(bar_yy[time_tart:time_end]['y_hat'].index,
           bar_yy[time_start:time_end]['y_hat'].values,
           width =0.24,
           align='center', alpha=0.6, color='b')
    plt.savefig('THIS_IS_A_TEST.png')

if __name__ == "__main__":
    make_dash_board()






    '''
    pickle_model_name = 'gbr_2.pkl'
    model = unpickle_model(pickle_model_name)

    buoyID = 46059
    get_prediction_data(buoyID)
    prediction_df = clean_prediction_data('../data/data_for_prediction_{}.csv'.format(buoyID))
    prediction_df = adding_speed_col(prediction_df, 650)
    prediction_df = add_time_delta(prediction_df)
    prediction_df = add_time_y(prediction_df)
    prediction_df = round_time_y(prediction_df)
    prediction_df.to_csv('../data/prediction_df.csv')

    prediction_df['ID'] = 46059

    cols_to_keep = ['YY', 'MM', 'DD', 'hh', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD',
                'APD', 'PRES', 'ATMP', 'WTMP', 'DEWP', 'ID', 't_arrive']

    X_real_time_predictions = prediction_df[cols_to_keep].values

    # real time predictions at nearshore from the offshore conditions at offshore buoy 46059
    y_hat_realtime = model.predict(X_real_time_predictions)

    # adding the model predicted data to the dataframe
    prediction_df['y_hat'] = y_hat_realtime

    # making the prediction df index to 'time_y_hr'
    prediction_df.index = prediction_df['time_y_hr']

    # resampling the the data frame by the hour
    yy_resample = prediction_df.resample('H').mean()

    # adding an hour col to the df to parse it by 6am, 12pm and 6pm
    yy_resample['date_fig'] = yy_resample.index
    yy_resample['hr_fig'] = yy_resample['date_fig'].apply(lambda x: x.hour)
    bar_yy = yy_resample[(yy_resample['hr_fig']==6) | (yy_resample['hr_fig']==12) | (yy_resample['hr_fig']==18)]

    # interpolating to fill in the missing gaps
    bar_yy = bar_yy.interpolate(method='linear', axis=0).bfill()
    '''
