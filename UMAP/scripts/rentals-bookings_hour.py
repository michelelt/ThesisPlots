import pandas as pd
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    with open('../config.json') as fp: config = json.load(fp)
    nrows=100000

    c2g = pd.read_csv(config['data_path']+'Torino.csv', nrows=nrows)
    # c2g = c2g[(c2g.init_time >= config['init_ts']) & (c2g.final_time <= config['final_ts']) ]
    c2g['Date_index'] = pd.to_datetime(c2g.init_date, format='%Y-%m-%d %H:%M:%S')
    c2g['Wod'] = c2g.Date_index.dt.weekday_name
    c2g = c2g[c2g['distance']>=config['distance_m_min']]
    c2g_we = c2g[c2g['Wod'].isin(['Sunday', 'Saturday'])]
    c2g_wd = c2g[~c2g['Wod'].isin(['Sunday', 'Saturday'])]
    c2g_number_of_workingdays = c2g_wd.groupby('Wod').count()['_id'].sum()
    c2g_number_of_workingends = c2g_we.groupby('Wod').count()['_id'].sum()


    enj = pd.read_csv(config['data_path']+'enjoyTorino.csv', nrows=nrows)
    # enj = enj[ (enj.final_time <= config['final_ts'])  ]
    enj['Date_index'] = pd.to_datetime(enj.init_date, format='%Y-%m-%d %H:%M:%S')
    enj['Date'] = enj.Date_index.dt.date
    enj['Wod'] = enj.Date_index.dt.weekday_name
    enj = enj[enj['distance'] >= config['distance_m_min']]
    enj_we = enj[enj['Wod'].isin(['Sunday', 'Saturday'])]
    enj_wd = enj[~enj['Wod'].isin(['Sunday', 'Saturday'])]
    enj_number_of_workingdays = enj_wd.groupby('Wod').count()['_id'].sum()
    enj_number_of_workingends = enj_we.groupby('Wod').count()['_id'].sum()


    c2g_we = c2g_we.groupby('Hour').count()['_id']
    c2g_wd = c2g_wd.groupby('Hour').count()['_id']
    enj_we = enj_we.groupby('Hour').count()['_id']
    enj_wd = enj_wd.groupby('Hour').count()['_id']


    fig, ax = plt.subplots(1,1, figsize=(16,9))
    ax.plot(c2g_wd.index, c2g_wd.values, color='blue', label='Car2go Working Days')
    ax.plot(c2g_we.index, c2g_we.values, color='blue', label='Car2go Week Ends', linestyle='--')
    ax.plot(enj_wd.index, enj_wd.values, color='red', label='Enjoy Working Days')
    ax.plot(enj_we.index, enj_we.values, color='red', label='Enjoy Week Ends', linestyle='--')
    ax.tick_params(axis='x', rotation=15)
    ax.legend()
    ax.grid()
    # ax.set_ylim(0,6000)

    plt.savefig(config['output_plot_path'] + 'ReB_Hour.pdf', bboxinches='tight')
