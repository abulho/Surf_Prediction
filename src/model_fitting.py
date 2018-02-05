#Importing required Python packages
import numpy as np
from sklearn import metrics
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error, r2_score
from get_train_test_for_modeling import *
import multiprocessing

def model(X_train, y_train):

    '''
    This function take in X and y for training
    and will fit a gradient boosted regressor model
    and return the model

    input:
    X_train, y_train

    output:
    gradient boosted regressor model that is fit

    '''
    n_estimators = 60000
    params = {'n_estimators': n_estimators,
              'max_depth': 3,
              'min_samples_split': 4,
              'learning_rate': 0.01,
              'loss': 'ls'}

    gbr = GradientBoostingRegressor(**params)
    gbr.fit(X_train, y_train.ravel())

    return gbr


def pickle_model(filename_to_save, model):
    '''
    this function will take in a fitted model and save pickle model
    to the directory

    input:
    fitted model

    output:
    pickle model

    '''
    with open(filename_to_save, 'wb') as f:
       # Write the model to a file.
       pickle.dump(model, f)

def get_X_y_for_hr(hour):
    '''
    take in the hour to make the train and test data for

    input:
    should be on of the following:
    'hr', '24hr', '48hr', '72hr', '96hr', '120hr', '144hr'

    output:
    the corresponding train and test data for the hour that was input
    '''
    filename = 'data_X_y_46059_' + hour + '.csv'
    Xy_df = get_Xy_data(filename)

    cols_to_keep = ['YY_x', 'MM_x', 'DD_x', 'hh_x', 'WD_x', 'WSPD_x',
                'GST_x', 'WVHT_x', 'DPD_x', 'APD_x', 'MWD_x', 'BAR_x', 'ATMP_x',
                'WTMP_x', 'DEWP_x', 'ID_x', 't_arrive', 'WVHT_y']

    train_yrs = [1995, 1996, 1997, 1998, 1999, 2000, 2003, 2004, 2006, 2007]
    test_yrs  = [2008]

    X_train, X_test, y_train, y_test = get_train_test(Xy_df, cols_to_keep, train_yrs, test_yrs)

    return X_train, X_test, y_train, y_test

def model_fit_and_pickle(suffix):
    print('Fitting and Pickling {} Model'.format(suffix))
    pickle_name = 'gbr_' + suffix + '.pkl'
    X_train, X_test, y_train, y_test = get_X_y_for_hr(suffix)
    gbr = model(X_train, y_train)
    pickle_model(pickle_name, gbr)

    return gbr

def main():
    suffix = ['hr', '24hr', '48hr', '72hr', '96hr', '120hr', '144hr']
    prefix = 'data_X_y_46059_'
    n_jobs = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes = n_jobs)
    models = pool.map(model_fit_and_pickle, suffix)

if __name__ == '__main__':
    main()
