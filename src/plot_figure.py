import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from make_null import *

plt.style.use('ggplot')

def plot_figures(filename, yearbegin=None, yearend=None):
    '''
    input:
    takes in a csv file name

    output:
    output will be plots specified in plots cols

    '''
    data_df = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')
    data_df = making_null_values(data_df)

    # subsetting the data frames based on year begin and year end
    years = [year for year in range(yearbegin, yearend + 1)]

    temp = []
    for year in years:
        temp.append(data_df[data_df['YY'] == year]) # getting the data frame corresponding to the year
    data_df_plot = pd.concat(temp, axis = 0)

    plot_cols = ['WD', 'WSPD', 'WVHT', 'DPD']

    figure, axes = plt.subplots(4,sharex=True, figsize=(15,8))

    for item, ax in zip(plot_cols, axes.flatten()):
        data_df_plot[item].plot(ax=ax, alpha=0.8)
        #ax.plot(data_df_plot[item], alpha=0.8)
        ax.set_ylabel(item)
        plt.suptitle(filename.split('.')[0])
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    return ax

if __name__ == "__main__":
    #filename = ['data_46078.csv', 'data_46066.csv', 'data_46075.csv', 'data_46070.csv']
    #filename = ['data_46005.csv', 'data_46002.csv', 'data_46059.csv', 'data_46006.csv']
    filename = ['data_46026.csv']
    start = 2007
    end = 2009
    for item in filename:
        print('plotting and saving time series from {} to {} for {}'.format(start, end,item))
        plot_figures(item, start, end)
        plt.savefig('Figure_' + item.split('.')[0] + '.png')
