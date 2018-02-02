import pickle

def unpickle_model(pickle_model_name):
    with open(pickle_model_name, 'rb') as f:
        model = pickle.load(f)
    return model

if __name__ == "__main__":
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

    
