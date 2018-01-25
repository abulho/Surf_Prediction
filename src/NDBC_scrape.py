import os
import requests
import time
from bs4 import BeautifulSoup

def buoy_num_start_end(filename):
    '''
    input:
    takes in a csv file with the bouy number, start and end year for the available data

    output:
    a dictionary. Key is the buoy number and the values are start year and end year

    '''

    with open(filename) as f:
        data = f.readlines()

    buoy_dict = dict()
    for item in data:
        temp_data = item.rstrip().split()
        buoy_dict[temp_data[0]] = [temp_data[1], temp_data[2]]

    return buoy_dict

def make_url(number, year):
    '''
    input:
    buoy number and year

    output:
    url to go to, in order to get the data for the given buoy number and year

    '''
    urlname_part1 = 'http://www.ndbc.noaa.gov/view_text_file.php?'
    urlname_part2 = 'filename={}h{}.txt.gz&dir=data/historical/stdmet/'.format(number.lower(), year)
    return urlname_part1 + urlname_part2

def get_buoy_data(filename):
    '''
    input:
    takes in the csv file with buoy number and date start of data and date end of data

    ouput:
    buoy data as csv files

    '''

    bouydict = buoy_num_start_end(filename)

    for k, v in bouydict.items():

        date_range = range(int(v[0]), int(v[1])+1)

        print('Downloading data from bouy : {}'.format(k))

        path = 'data_' + k #making the directory name

        if not os.path.exists(path):
            os.makedirs(path)

        for year in date_range:

            filename_to_save = str(k) + str(year) #making the file name
            path_filename = os.path.join(path, filename_to_save) #making the file name with directory

            if os.path.isfile(path_filename):
                print('File already present for buoy {} and year {}'.format(k, year))
                continue
            else:
                print('Downloading data from bouy {} and  year {}'.format(k, year))
                time.sleep(10) # adding a six second delay before each request
                url = make_url(k, year)
                content = requests.get(url)

                filename_to_save = str(k) + str(year)
                with open(os.path.join(path,filename_to_save), 'w') as f:
                    f.write(content.text)

if __name__ == '__main__':
    get_buoy_data('buoy_data_dates.csv')
    #buoy_num_start_end('buoy_data_dates.csv')
