from get_train_test_for_modeling import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, r2_score
from format_train_test import *
import pickle
import sklearn.cross_validation as cv
from sklearn.ensemble import (GradientBoostingRegressor,
                              GradientBoostingClassifier,
                              AdaBoostClassifier,
                              RandomForestClassifier)
import time

def make_cv_data_sets(dataframe, cols_to_keep, allyrs):
    X_train_sets = []
    y_train_sets = []
    X_test_sets  = []
    y_test_sets  = []
    for year in allyrs:
        test_yr = [year]
        train_yr =[yr for yr in allyrs if yr != year]
        X_train, X_test, y_train, y_test = get_train_test(Xy_df, cols_to_keep, train_yr, test_yr)
        X_train_sets.append(X_train)
        y_train_sets.append(y_train)
        X_test_sets.append(X_test)
        y_test_sets.append(y_test)
    return X_train_sets, y_train_sets, X_test_sets, y_test_sets

def grid_fit(x_train, y_train, x_test, y_test, param_grid):

        models = [GradientBoostingRegressor(n_estimators = 10000,
                                            max_depth = td,
                                            learning_rate = 0.0001,
                                            subsample = 0.5,
                                            loss ='ls') for td in param_grid.values()[0]]

        processes = [mp.Process(target = model.fit, args=(x_train,y_train)) for model in models]

        for p in processes:
            p.start
        for p in processes:
            p.join

        N_ESTIMATORS = 1000
        N_FOLDS = 10

        tree_depths = [1, 3, 5]
        N_TREE_DEPTHS = len(tree_depths)

        test_scores = np.zeros((N_FOLDS, N_TREE_DEPTHS, N_ESTIMATORS))
        train_scores = np.zeros((N_FOLDS, N_TREE_DEPTHS, N_ESTIMATORS))
        #rmse_train = [mean_squared_error(y_train, model.predict(x_train)) ** 0.5 for model in models]
        #rmse_test  = [mean_squared_error(y_test, model.predict(x_test)) ** 0.5 for model in models]
        for i, model in enumerate(models):

            for j, y_pred in enumerate(zip(model.staged_predict(X_train), model.staged_predict(X_test))):

                train_scores[k, i, j] = model.loss_(y_train, y_pred[0])
                test_scores[k, i, j] = model.loss_(y_test, y_pred[1])

                print('fitting and predicting for tree depth {}, Train: {}, Test: {}'.format(tree_depths[i]),
                                                                                             model.loss_(y_train,
                                                                                                         y_pred[0]),
                                                                                             model.loss_(y_test,
                                                                                                         y_pred[1]))
        return train_scores, test_scores

if __name__ == '__main__':
    start = time.time()
    filename = 'data_X_y_46059_hr.csv'
    Xy_df = get_Xy_data(filename)

    cols_to_keep = ['YY_x', 'MM_x', 'DD_x', 'hh_x', 'WD_x', 'WSPD_x',
                    'GST_x', 'WVHT_x', 'DPD_x', 'APD_x', 'BAR_x', 'ATMP_x',
                    'WTMP_x', 'DEWP_x', 'ID_x', 't_arrive','WVHT_y']

    allyrs = [1995, 1996, 1997, 1998, 1999, 2000, 2003, 2004, 2006, 2007, 2008]

    X_train_sets, y_train_sets, X_test_sets, y_test_sets = make_cv_data_sets(Xy_df, cols_to_keep, allyrs)


    param_grid = {'tree_depth':[3,5,7]}
    processes = [mp.Process(target = grid_fit,
                            args=(x_train, y_train, x_test, y_test, param_grid))
                            for x_train, y_train, x_test, y_test in zip(X_train_sets, y_train_sets, X_test_sets, y_test_sets)]
    print(time.time()-start)
