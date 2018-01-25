import pandas as pd
import numpy as np
import os
import glob
import time

def concat_all_data(foldername):
    '''
    input:
    file path where the data files are located for concating

    output:
    single csv file with all the files joined together

    '''

    files = os.listdir(foldername)

    data_df_list = []
    col_names_final = ['YY', 'MM', 'DD', 'hh', 'WD', 'WSPD', 'GST', 'WVHT',
                      'DPD', 'APD','MWD', 'BAR', 'ATMP', 'WTMP', 'DEWP', 'VIS']

    for data_file in files:

        data = pd.read_csv(os.path.join(foldername, data_file), sep='\s+')
        if len(data) == 0:
            continue
        col_names = data.columns

        print('analysis data file {}'.format(data_file))

        if col_names[0] != '#YY':
            data_to_save = pd.read_csv(os.path.join(foldername, data_file), sep='\s+', header=[0])
            col_names_new = data_to_save.columns
            if 'mm' in col_names_new:
                data_to_save.drop(columns='mm', inplace = True)
            if 'TIDE' in col_names_new:
                data_to_save.drop(columns='TIDE', inplace = True)
            data_to_save.columns = col_names_final
            data_df_list.append(data_to_save)
        else:
            data_to_save = pd.read_csv(os.path.join(foldername, data_file), sep='\s+', header=[1])
            col_names_new = data_to_save.columns
            if 'mn' in col_names_new:
                data_to_save.drop(columns='mn', inplace = True)
            if 'ft' in col_names_new:
                data_to_save.drop(columns='ft', inplace = True)
            data_to_save.columns = col_names_final
            data_df_list.append(data_to_save)

        data_concat_df = pd.concat(data_df_list, axis = 0)
        data_concat_df.to_csv(foldername + '.csv', index = False)

if __name__ == '__main__':
    directory = os.getcwd()
    alldir = glob.glob(directory + '/*/')

    temp_list = [direc.split('/')[-2] for direc in alldir]
    dir_list = [x for x in temp_list if 'data' in x ]

    for folder in dir_list:
        print('Anlyzing the files in the folder {}'.format(folder))
        if folder + '.csv' in glob.glob('*.csv'):
            print('file : {} already exist'.format(folder + '.csv'))
            print('*' * 30)
            continue
        else:
            concat_all_data(folder)
