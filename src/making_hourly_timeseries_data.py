import pandas as pd
import numpy as np
import datatime

import pandas as pd
import numpy as np
import datetime

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
