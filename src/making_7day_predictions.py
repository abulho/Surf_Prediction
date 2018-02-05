from get_prediction_data import *
import datetime
import pickle

def unpickle_model(pickle_model_name):
    '''
    take in the pickle model and return the unpickle version of it

    input:
    pickle model

    output:
    unpickle model

    '''
    with open(pickle_model_name, 'rb') as f:
        model = pickle.load(f)
    return model

def fit_to_real_time(model_name):
    print('unpickling and making predictions for {} ...'.format(datecol[i]))

if __name__ == '__main__':

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
                    'APD','MWD', 'PRES', 'ATMP', 'WTMP', 'DEWP', 'ID', 't_arrive']

    predict_hrs = [hr for hr in range(24,166,24)]
    for hr in predict_hrs:
        prediction_df['time_delta_{}'.format(str(hr))] = prediction_df['t_arrive'].apply(lambda x: datetime.timedelta((x+hr)/24))
        prediction_df['time_y_{}'.format(str(hr))] = prediction_df.index + prediction_df['time_delta_{}'.format(hr)]
        prediction_df['time_y_hr_{}'.format(hr)]  = prediction_df['time_y_{}'.format(hr)].apply(lambda dt: datetime.datetime(dt.year,
                                                                                                 dt.month,
                                                                                                 dt.day,
                                                                                                 dt.hour,
                                                                                                 0,0))
    X_real_time_predictions = prediction_df[cols_to_keep].values

    pkl_lst = ['gbr_hr.pkl','gbr_24hr.pkl','gbr_48hr.pkl','gbr_72hr.pkl',
               'gbr_96hr.pkl','gbr_120hr.pkl', 'gbr_144hr.pkl']

    datecol = ['hr', 'hr_24', 'hr_48', 'hr_72', 'hr_96', 'hr_120', 'hr_144']

    date_today = datetime.datetime.now().date() # gives todays date
    tdel = [0, 24, 48, 72, 96, 120, 144] # hours of predictions

    df_lst_7day_pred = []
    for i, model in enumerate(pkl_lst):

        print('unpickling and making predictions for {} ...'.format(datecol[i]))

        t_parse = (date_today + datetime.timedelta(tdel[i]/24)).strftime('%Y%m%d')

        date_col = 'time_y_' + datecol[i]
        gbr = unpickle_model(model)
        y_hat = gbr.predict(X_real_time_predictions)
        df = prediction_df[[date_col]]
        df['yhat'] = y_hat
        df['offshore_date'] = df.index
        df.index = df[date_col]

        if i == 0:
            df_2_app = df[:t_parse]
        else:
            df_2_app = df[t_parse:]

        df_lst_7day_pred.append(df_2_app)

    print('Saving Predictions...')

    df_7day_pred = pd.concat(df_lst_7day_pred, axis=0)
    df_7day_pred .index.name='Date'
    df_7day_pred.to_csv('predictions_7days.csv')
