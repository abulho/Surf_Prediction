import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

def get_tide_data(stationid, year):
    '''
    input:
    tide station id
    year --> Ex: 1995

    output:
    csv file with the tide levels
    '''

    a = "https://tidesandcurrents.noaa.gov/api/"
    b = "datagetter?begin_date={}0101 00:00&end_date={}1231 23:00&".format(year, year)
    c = "station={}&product=hourly_height&datum=mllw&units=metric&".format(stationid)
    d = "time_zone=lst_ldt&application=web_services&format=json "

    url = a + b + c + d

    time.sleep(6)

    data = requests.get(url)
    data_tide = data.json()
    tidedf = pd.DataFrame(data_tide['data'])
    tidedf.drop(columns=['f','s'], inplace=True)
    cols = ['Date', 'WaterLevel']
    tidedf.columns = cols
    tidedf['WaterLevel'] = tidedf['WaterLevel'].apply(lambda x: float(x))

    return tidedf

if __name__ == '__main__':

    yr_lst = [1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
              2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,2013]

    temp_df = []
    for year in yr_lst:
        print('Getting tide data for st:9414290 yr:{}'.format(year))
        df = get_tide_data(9414290, year)
        temp_df.append(df)

    tide_df = pd.concat(temp_df, axis = 0)
    tide_df.to_csv('tides.csv', index=False)
