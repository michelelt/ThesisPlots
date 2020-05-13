import sys
sys.path.append('../..')
from Classes.Filter import Filter
from Classes.ReadConfig import ReadConfig
from Classes.DF2GDF import DF2GDF
from Classes.Loader import Loader

import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt


if __name__=='__main__':
    rc = ReadConfig('../config.json')
    config = rc.get_config()
    plt.rcParams.update({'font.size': config['fs']})

    city = 'Torino'
    nrows = 100000
    provider = 'both'

    df = Loader(config, city, provider, nrows)
    

    filter = Filter(df, config)
    df_before_filters = df.copy()
    filter.date_standardization()
    filter.remove_fake_bookings_torino()
    df = filter.rentals()
    df = df[df['pt_duration']!=-1]
    df = df[df['driving_duration']!=-1]

    c2g = df[df.vendor=='car2go']
    c2g = c2g.groupby('Hour').median()['duration'].div(60)
    enj = df[df.vendor == 'enjoy']
    enj = enj.groupby('Hour').median()['duration'].div(60)
    drv = df.groupby('Hour').median()['driving_duration'].div(60)
    pt = df.groupby('Hour').median()['pt_duration'].div(60)

    fig,ax = plt.subplots(1,1,figsize=config['figsize'])
    ax.plot(c2g, color='blue', marker='o', label='Car2go')
    ax.plot(enj, color='red', marker='o', label='Enjoy')
    ax.plot(drv, color='green', marker='o', label='Driving')
    ax.plot(pt, color='purple', marker='o', label='PT')

    ax.grid()
    ax.legend()

    fig.show()

