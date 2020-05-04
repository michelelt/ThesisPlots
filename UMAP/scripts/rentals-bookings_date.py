import sys
sys.path.append('../..')
from Classes.ReadConfig import ReadConfig

import pandas as pd
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    rc = ReadConfig('../config.json')
    config = rc.get_config()

    nrows=100000

    c2g = pd.read_csv(config['data_path']+'Torino.csv', nrows=nrows)
    # c2g = c2g[(c2g.init_time >= config['init_ts']) & (c2g.final_time <= config['final_ts']) ]
    c2g['Date_index'] = pd.to_datetime(c2g.init_date, format='%Y-%m-%d %H:%M:%S')
    c2g['Date'] = c2g.Date_index.dt.date
    c2g_r = c2g[(c2g.distance > 0)]

    enj = pd.read_csv(config['data_path']+'enjoyTorino.csv', nrows=nrows)
    # enj = enj[ (enj.final_time <= config['final_ts'])  ]
    enj['Date_index'] = pd.to_datetime(enj.init_date, format='%Y-%m-%d %H:%M:%S')
    enj['Date'] = enj.Date_index.dt.date
    enj_r = enj[(enj.distance > 0)]


    c2g_b = c2g.groupby('Date').count().sort_index()
    c2g_r = c2g_r.groupby('Date').count().sort_index()
    enj_b = enj.groupby('Date').count().sort_index()
    enj_r = enj_r.groupby('Date').count().sort_index()


    min_date = min(c2g.Date.min(), enj.Date.min())
    max_date = max(c2g.Date.max(), enj.Date.max())
    date_list = pd.DataFrame(pd.date_range(min_date, max_date), columns=['Date_list'])
    date_labels = date_list['Date_list'].dt.strftime('%b \'%y').drop_duplicates().reset_index().drop('index', axis=1)
    date_list['Date_list'] = date_list['Date_list'].dt.date

    c2g_b = date_list.merge(c2g_b, how='left', left_on='Date_list', right_index=True).set_index('Date_list')['_id']
    c2g_r = date_list.merge(c2g_r, how='left', left_on='Date_list', right_index=True).set_index('Date_list')['_id']
    enj_b = date_list.merge(enj_b, how='left', left_on='Date_list', right_index=True).set_index('Date_list')['_id']
    enj_r = date_list.merge(enj_r, how='left', left_on='Date_list', right_index=True).set_index('Date_list')['_id']

    fig, ax = plt.subplots(1,1, figsize=config['figsize'])
    ax.plot(c2g_b.index, c2g_b.values, color='blue', label='Car2go Bookings')
    ax.plot(c2g_r.index, c2g_r.values, color='blue', label='Car2go Rentals', linestyle='--')
    ax.plot(enj_b.index, enj_b.values, color='red', label='Enjoy Bookings')
    ax.plot(enj_r.index, enj_r.values, color='red', label='Enjoy Rentals', linestyle='--')
    # ax.set_xticks(date_labels.index)
    ax.set_xticklabels(date_labels.Date_list.tolist())
    ax.tick_params(axis='x', rotation=15)
    ax.legend()
    ax.grid()
    ax.set_ylim(0,6000)

    plt.savefig(config['output_plot_path'] + 'ReB_date.pdf', bboxinches='tight')
    fig.show()


