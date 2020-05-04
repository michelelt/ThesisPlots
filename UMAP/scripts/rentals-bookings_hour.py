import sys
sys.path.append('../..')
from Classes.ReadConfig import ReadConfig
from Classes.Filter import Filter


import pandas as pd
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    rc = ReadConfig('../config.json')
    config = rc.get_config()
    nrows=100000

    c2g = pd.read_csv(config['data_path']+'Torino.csv', nrows=nrows)
    c2g_filter = Filter(c2g, config)
    c2g = c2g_filter.date_standardization()
    c2g = c2g[~c2g.index.isin(c2g_filter.reservation('car2go').index)]
    c2g_split_dict = c2g_filter.split_WD_WE()
    c2g_we = c2g_split_dict['df_we']
    c2g_wd = c2g_split_dict['df_wd']
    c2g_number_of_workingdays = c2g_wd.groupby('Wod').count()['_id'].sum()
    c2g_number_of_weekends = c2g_we.groupby('Wod').count()['_id'].sum()

    enj = pd.read_csv(config['data_path']+'enjoyTorino.csv', nrows=nrows)
    enj_filter = Filter(c2g, config)
    enj = enj_filter.date_standardization()
    enj = enj[~enj.index.isin(enj_filter.reservation('enjoy').index)]
    enj_split_dict = enj_filter.split_WD_WE()
    enj_we = enj_split_dict['df_we']
    enj_wd = enj_split_dict['df_wd']
    enj_number_of_workingdays = enj_wd.groupby('Wod').count()['_id'].sum()
    enj_number_of_weekends = enj_we.groupby('Wod').count()['_id'].sum()



    c2g_we = c2g_we.groupby('Hour').count()['_id']
    c2g_wd = c2g_wd.groupby('Hour').count()['_id']
    enj_we = enj_we.groupby('Hour').count()['_id']
    enj_wd = enj_wd.groupby('Hour').count()['_id']


    fig, ax = plt.subplots(1,1, figsize=config['figsize'])
    ax.plot(c2g_wd.index, c2g_wd.values, color='blue', label='Car2go Working Days')
    ax.plot(c2g_we.index, c2g_we.values, color='blue', label='Car2go Week Ends', linestyle='--')
    ax.plot(enj_wd.index, enj_wd.values, color='red', label='Enjoy Working Days')
    ax.plot(enj_we.index, enj_we.values, color='red', label='Enjoy Week Ends', linestyle='--')
    ax.tick_params(axis='x', rotation=15)
    ax.legend()
    ax.grid()
    # ax.set_ylim(0,6000)

    plt.savefig(config['output_plot_path'] + 'ReB_Hour.pdf', bboxinches='tight')
    fig.show()
