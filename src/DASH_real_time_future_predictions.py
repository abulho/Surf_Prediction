from datetime import date
from datetime import datetime
from datetime import timedelta
import matplotlib
import pandas as pd
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

all_pred_df = pd.read_csv('predictions_7days.csv', parse_dates=['Date'], index_col='Date')
all_pred_df = all_pred_df.resample('H').mean()

# adding an hour col to the df to parse it by 6am, 12pm and 6pm
all_pred_df['date_fig'] = all_pred_df.index
all_pred_df['hr_fig'] = all_pred_df['date_fig'].apply(lambda x: x.hour)
bar_yy = all_pred_df[(all_pred_df['hr_fig']==6) | (all_pred_df['hr_fig']==12) | (all_pred_df['hr_fig']==18)]
bar_yy = all_pred_df[(all_pred_df['hr_fig']==6) | (all_pred_df['hr_fig']==12) | (all_pred_df['hr_fig']==18)]

# interpolating to fill in the missing gaps
bar_yy = bar_yy.interpolate(method='linear', axis=0).bfill()

def make_plot_times():
    dt = datetime.now().date()
    time_start = dt + timedelta(hours = 0)
    time_end = dt + timedelta(hours = 144)

    return time_start, time_end

def make_dash_board():
    '''
    input:
    pred_data = data frame with predictions

    output:
    graphic for dash board

    '''
    print('Making Dash board...')

    myFmt = mdates.DateFormatter('%H:%S')

    time_start, time_end = make_plot_times()

    t1 = time_start.strftime('%Y%m%d')
    t2 = time_end.strftime('%Y%m%d')

    fig, ax = plt.subplots(figsize=(25,6))
    ax.bar(bar_yy[t1:t2]['yhat'].index.to_pydatetime(),
           bar_yy[t1:t2]['yhat'].values,
           width=0.24,
           align='center',
           alpha=0.6,
           color='b')

    plt.xticks(bar_yy[t1:t2]['yhat'].index.to_pydatetime())
    ax.xaxis.set_major_formatter(myFmt)
    plt.xticks(rotation=90)
    ax.set_ylim(0,5)

    # set individual bar lables using above list
    for j, i in enumerate(ax.patches):
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()+0.035, i.get_height()+.05, \
                str(round(bar_yy[t1:t2]['yhat'].values[j],1)), fontsize=18,
                    color='red')

    weekday_dict={0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    for j, i in enumerate(ax.patches[0::3]):
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()+0.13, 4.6, \
                weekday_dict[bar_yy[t1:t2]['yhat'][0::3].index[j].weekday()], fontsize=20,
                    color='black')

    for j, i in enumerate(ax.patches[0::3]):
        # get_x pulls left or right; get_height pushes up or down
        month = bar_yy[t1:t2]['yhat'][0::3].index[j].month
        day = bar_yy[t1:t2]['yhat'][0::3].index[j].day

        ax.text(i.get_x()+0.18, 4.35,
                str(month)+'/'+str(day),
                fontsize=15,color='black')

    ax.tick_params(axis='x', labelsize=18, color='black')
    ax.tick_params(axis='y', labelsize=18, color= 'black')
    ax.set_ylabel('Wave Height (m)', fontsize=20, color='black')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.set_facecolor('white')
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('blue')
    ax.spines['left'].set_color('blue')
    plt.tight_layout()
    plt.savefig('../FlaskApp/surfapp-1/static/DASH_BOARD.png')

    print('Complete.')

    return plt

if __name__ == "__main__":
    make_dash_board()
