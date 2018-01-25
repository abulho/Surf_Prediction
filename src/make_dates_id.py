import pandas as pd
import os
import glob
from datetime import date
from datetime import datetime

def make_dates_id(folder, filename):
    path = os.path.join(folder, filename)
    data = pd.read_csv(path)
    mask = (data['YY'] < 1999)
    data.loc[mask,['YY']] = data.loc[mask,['YY']].apply(lambda x: x+1900)
    dates_temp = data[['YY','MM','DD','hh']].values
    new_date = [datetime(*x) for x in dates_temp]
    data['Date'] = new_date
    data['ID'] = filename.split('.')[0].split('_')[1].lower()
    print('Adding the  date and saving the data for buoy : {}'.format(filename))
    print('*' * 30)
    data.to_csv(path, index = False)

if __name__ == '__main__':

    directory = os.getcwd()
    allfiles= glob.glob('data_*.csv')

    file_list = [x for x in allfiles if 'data' in x]

    for data_file in file_list:
        make_dates_id(directory, data_file)
