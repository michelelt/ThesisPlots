import sys
sys.path.append('../..')
from Classes.Filter import Filter
from Classes.DF2GDF import DF2GDF
from Classes.ReadConfig import ReadConfig


import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt

if __name__=='__main__':
    rc = ReadConfig('../config.json')
    config = rc.get_config()
    plt.rcParams.update({'font.size': config['fs']})

    nrows = 128000
    provider = 'both'

    if provider == 'car2go': df = pd.read_csv(config['data_path'] + 'Torino.csv', nrows=nrows)
    elif provider=='both':
        df=pd.read_csv(config['data_path'] + 'Torino.csv', nrows=nrows)\
        .append(pd.read_csv(config['data_path'] + 'enjoyTorino.csv', nrows=nrows), ignore_index=True, sort=False)
    else: df = pd.read_csv(config['data_path'] + 'enjoyTorino.csv', nrows=nrows)

    df_before_filters = df.copy()

    filter = Filter(df, config)
    filter.remove_fake_bookings_torino()
    filter.date_standardization()
    df = filter.rentals()
    df = df[df['pt_duration']!=-1]

    # # apply time bin to pt
    df['TimeBin'] = None
    df['pt_duration'] = df['pt_duration'].div(60)
    labels=[]
    for tb in range(0,11):
        indeces_to_acces = df[(df.pt_duration >= 5*tb) & (df.pt_duration < 5*(tb+1) )].index
        if tb == 10: indeces_to_acces = df[(df.pt_duration >= 5*tb)].index
        df.loc[indeces_to_acces, 'TimeBin'] = tb
        if tb == 10: labels.append('%d+'%(5*tb))
        else: labels.append('%d-%d'%(5*tb, 5*(tb+1)))

    c2g = df[df.vendor=='car2go']
    tot_c2g = len(c2g)
    enj = df[df.vendor=='enjoy']
    tot_enj = len(enj)

    c2g = c2g.groupby('TimeBin').count()['_id'].div(tot_c2g).mul(100)
    enj = enj.groupby('TimeBin').count()['duration'].div(tot_enj).mul(100)

    tot = pd.concat([c2g, enj], axis=1)
    tot = tot.rename(columns={'_id':'Car2go', 'duration':'Enjoy'}).reset_index()


    fig, ax = plt.subplots()
    tot.plot(ax=ax, x='TimeBin', y=['Car2go', 'Enjoy'], kind='bar', color=['blue', 'red'], rot=15)
    ax.grid()
    ax.set_xticklabels(labels)

    fig.show()
