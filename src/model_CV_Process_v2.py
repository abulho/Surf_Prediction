from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
import pandas as pd
import numpy as np
from sklearn.externals import joblib

def model_grid_search(X_train, y_train):
    model = GradientBoostingRegressor()
    n_estimators = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 50000, 60000]
    learning_rate = [0.00001, 0.0001, 0.001, 0.01, 0.1]
    param_grid = dict(learning_rate=learning_rate, n_estimators=n_estimators)
    kfold = KFold(n_splits=12, shuffle=False)
    grid_search = GridSearchCV(model,
                               param_grid,
                               scoring="neg_mean_squared_error",
                               n_jobs=-1,
                               cv=kfold,
                               verbose=1)

    grid_search.fit(X_train, y_train.ravel())

    joblib.dump(grid_search, 'grid_search_all.pkl')
    joblib.dump(grid_search.best_estimator_, 'grid_search_best.pkl')

    return grid_search

def get_train_test_for_cv(dataframe, cols_to_keep, train_yrs):
    '''
    input:
    dataframe
    list of cosl to drop
    make sure predictor is the last col

    output:
    X --> training
    y --> training
    X --> testing
    y --> testing

    '''
    X_y_data = dataframe
    X_y_interp = X_y_data.interpolate(method='linear', axis=0).bfill()

    dfXy = X_y_interp[cols_to_keep]

    train_lst = []
    for year in train_yrs:
         train_lst.append(dfXy[dfXy['YY_x'] == year])
    train_df = pd.concat(train_lst, axis=0)

    X_train = train_df.values[:,:-1]
    y_train = train_df.values[:,-1:]

    return X_train, y_train

def get_Xy_data_for_cv(filename):
    data = pd.read_csv(filename)
    return data

if __name__ == "__main__":
    filename = 'data_X_y_46059_hr.csv'
    Xy_df = get_Xy_data_for_cv(filename)

    cols_to_keep = ['YY_x', 'MM_x', 'DD_x', 'hh_x', 'WD_x', 'WSPD_x',
                'GST_x', 'WVHT_x', 'DPD_x', 'APD_x', 'BAR_x', 'ATMP_x',
                'WTMP_x', 'DEWP_x', 'ID_x', 't_arrive', 'WVHT_y']

    train_yrs = [1995, 1996, 1997, 1998, 1999, 2000, 2003, 2004, 2006, 2007, 2008]
    X_train, y_train = get_train_test_for_cv(Xy_df, cols_to_keep, train_yrs)

    model_grid_search(X_train, y_train)
