import numpy as np
def making_null_values(dataframe):
    '''
    input:
    takes in a data frame

    output:
    output is a data frame with 99 and 999 vaules turned in to null values

    '''
    dataframe.replace(999, np.nan, inplace=True)
    dataframe.replace(99, np.nan, inplace=True)
    dataframe.replace(9999, np.nan, inplace=True)

    return dataframe
