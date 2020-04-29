import sys
sys.path.append('../..')
from Classes.Filter import Filter
from Classes.DF2GDF import DF2GDF


import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt

if __name__=='__main__':
    with open('../config.json') as fp : config = json.load(fp)
    nrows = 100000
    provider = 'car2go'

    if provider == 'car2go': df = pd.read_csv(config['data_path'] + 'Torino.csv', nrows=nrows)
    elif provider=='both':
        df=pd.read_csv(config['data_path'] + 'Torino.csv', nrows=nrows)\
        .append(pd.read_csv(config['data_path'] + 'enjoyTorino.csv', nrows=nrows), ignore_index=True, sort=False)
    else: df = pd.read_csv(config['data_path'] + 'enjoyTorino.csv', nrows=nrows)

    df['Date_index'] = pd.to_datetime(df.init_date, format='%Y-%m-%d %H:%M:%S')
    df['Date'] = df.Date_index.dt.date
    df["Wod"] = df.Date_index.dt.weekday_name
    df_before_filters = df.copy()

    filter = Filter(df, config)
    df = filter.remove_fake_bookings()
    split_df = filter.split_df(is_rental=True) #DURATION and DISTANCE filtering -> removing reservations and OL
    df = split_df['df_we'].append(split_df['df_wd'])


    df = df[df['driving_duration']!= -1]
    df['driving_duration'] = df['driving_duration'].div(60).astype(int)
    df['duration'] = df['duration'].div(60).astype(int)
    df = df.groupby(['duration', 'driving_duration']).count()['_id'].to_frame()

    pivot = pd.pivot_table(df, index='duration', columns='driving_duration', values='_id', fill_value=0)
    complete_pivot= pd.DataFrame(index=range(0,61), columns=range(0,61), data=0)
    pivot = complete_pivot+pivot
    pivot = pivot.fillna(0)

    fig, ax = plt.subplots()
    im = ax.imshow(pivot, cmap='Reds')
    ax.invert_yaxis()
    ax.plot([0, 50], [0, 50], linestyle='--')
    ax.set_xlim([0, 50])
    ax.set_ylim([0, 50])

    fig.tight_layout()

    plt.show()
    plt.savefig(config['output_plot_path']+'driving_vs_google_time.pdf')
