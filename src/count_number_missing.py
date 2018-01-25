import pandas as pd
from collections import defaultdict
import glob

def count_number_of_missing(filename):
    cols_to_consider = ['WD', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD']
    data = pd.read_csv(filename, parse_dates=['Date'])
    k = filename.split('.')[0].split('_')[1] # key for dict
    templst = []
    templst.append(len(data))
    for item in cols_to_consider:
        total_miss = data[(data[item] == 99.0) | (data[item] == 999)].count()
        templst.append(total_miss[0])
    return templst

if __name__ == '__main__':

     filename = glob.glob('data_*.csv')
     missing_dict = defaultdict(list)

     for data_file in filename:

         print('Finding the missing data for {}'.format(data_file))

         missing_counts = count_number_of_missing(data_file)
         k = data_file.split('.')[0].split('_')[1]

         for item in missing_counts:
             missing_dict[k].append(item)

     df_missing_counts =  pd.DataFrame(missing_dict)
     df_missing_counts.to_csv('missing_counts.csv')
