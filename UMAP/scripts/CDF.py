import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../..')

from Classes.Filter import Filter




def split_df(df, config, is_rental=True):
    if is_rental == True:
        df = df[df['distance'] >= config["distance_m_min"]]
        df = df[(df['duration'] >= config["duration_s_min"]) & (df['duration'] <= config["duration_s_max"])]
    else :
        df = df[df['distance'] == 0]
        df = df[(df['duration'] <= 60*30)]
    df_we = df[df.Wod.isin(["Saturday", "Sunday"])]
    df_wd = df[~df.Wod.isin(["Saturday", "Sunday"])]
    return df_we, df_wd

def compute_cdf(y_set):
    values = y_set
    sorted_data = np.sort(values)
    yvals = np.arange(len(values)) / float(len(values) - 1)
    return sorted_data, yvals


if __name__ = '__main__':
    with open('../config.json') as fp: config = json.load(fp)
    nrows=None


    c2g = pd.read_csv(config['data_path']+'Torino.csv', nrows=nrows)
    filter = Filter(c2g, config)
    c2g = filter.remove_fake_bookings()
    c2g['Date_index'] = pd.to_datetime(c2g.init_date, format='%Y-%m-%d %H:%M:%S')
    c2g['Date'] = c2g.Date_index.dt.date
    c2g["Wod"] = c2g.Date_index.dt.weekday_name
    c2g_b_we, c2g_b_wd = split_df(c2g, config, is_rental=False)
    c2g_r_we, c2g_r_wd = split_df(c2g, config, is_rental=True)



    enj = pd.read_csv(config['data_path']+'enjoyTorino.csv', nrows=nrows)
    filter = Filter(enj, config)
    enj = filter.remove_fake_bookings(enj, config)
    # enj = enj[ (enj.final_time <= config['final_ts'])  ]
    enj['Date_index'] = pd.to_datetime(enj.init_date, format='%Y-%m-%d %H:%M:%S')
    enj['Date'] = enj.Date_index.dt.date
    enj["Wod"] = enj.Date_index.dt.weekday_name
    enj_b_we, enj_b_wd = split_df(enj, config, is_rental=False)
    enj_r_we, enj_r_wd = split_df(enj, config, is_rental=True)



    '''
    cdf BOOKINGS DURATION -> does not produce a rental
    '''
    fig,ax = plt.subplots(1,1, figsize=(16,9))
    x_c2g_b_we, y_c2g_b_we = compute_cdf(c2g_b_we.duration)
    x_c2g_b_wd, y_c2g_b_wd = compute_cdf(c2g_b_wd.duration)

    x_enj_b_we, y_enj_b_we = compute_cdf(enj_b_we.duration)
    x_enj_b_wd, y_enj_b_wd = compute_cdf(enj_b_wd.duration)

    ax.plot(x_c2g_b_wd, y_c2g_b_wd, color='blue', label='Car2go Week Days')
    ax.plot(x_c2g_b_we, y_c2g_b_we, color='blue', linestyle='--', label="Car2go Week Ends")
    ax.plot(x_enj_b_wd, y_enj_b_wd, color='red', label='Enjoy Week Days')
    ax.plot(x_enj_b_we, y_enj_b_we, color='red', linestyle='--', label='Enjoy Week Ends')
    ax.grid()
    ax.legend()
    ax.set_xticks(range(0, 1801, 5*60))
    ax.set_xticklabels(range(0,31, 5))
    ax.set_xlabel("Duration [min]")
    ax.set_ylabel("ECDF")
    plt.savefig(config["output_plot_path"]+"CDF_Bookings_Duration.pdf", bbox_inches="tight")


    '''
    cdf RENTAL DURATION
    '''
    fig,ax = plt.subplots(1,1, figsize=(16,9))
    x_c2g_r_we, y_c2g_r_we = compute_cdf(c2g_r_we.duration)
    x_c2g_r_wd, y_c2g_r_wd = compute_cdf(c2g_r_wd.duration)

    x_enj_r_we, y_enj_r_we = compute_cdf(enj_r_we.duration)
    x_enj_r_wd, y_enj_r_wd = compute_cdf(enj_r_wd.duration)

    ax.plot(x_c2g_r_wd, y_c2g_r_wd, color='blue', label='Car2go Week Days')
    ax.plot(x_c2g_r_we, y_c2g_r_we, color='blue', linestyle='--', label="Car2go Week Ends")
    ax.plot(x_enj_r_wd, y_enj_r_wd, color='red', label='Enjoy Week Days')
    ax.plot(x_enj_r_we, y_enj_r_we, color='red', linestyle='--', label='Enjoy Week Ends')
    ax.grid()
    ax.legend()
    ax.set_xticks(range(0, 7201, 1200))
    ax.set_xticklabels(range(0,121, 20))
    ax.set_xlabel("Duration [min]")
    ax.set_ylabel("ECDF")
    plt.savefig(config["output_plot_path"]+"CDF_Rentals_Duration.pdf", bbox_inches="tight")


    '''
    cdf RENTAL DISTANCE
    '''
    fig,ax = plt.subplots(1,1, figsize=(16,9))
    x_c2g_r_we, y_c2g_r_we = compute_cdf(c2g_r_we.distance)
    x_c2g_r_wd, y_c2g_r_wd = compute_cdf(c2g_r_wd.distance)

    x_enj_r_we, y_enj_r_we = compute_cdf(enj_r_we.distance)
    x_enj_r_wd, y_enj_r_wd = compute_cdf(enj_r_wd.distance)

    ax.plot(x_c2g_r_wd, y_c2g_r_wd, color='blue', label='Car2go Week Days')
    ax.plot(x_c2g_r_we, y_c2g_r_we, color='blue', linestyle='--', label="Car2go Week Ends")
    ax.plot(x_enj_r_wd, y_enj_r_wd, color='red', label='Enjoy Week Days')
    ax.plot(x_enj_r_we, y_enj_r_we, color='red', linestyle='--', label='Enjoy Week Ends')
    ax.grid()
    ax.legend()
    ax.set_xticks(range(0, 20001, 5000))
    ax.set_xticklabels(range(0,21, 5))
    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("ECDF")
    plt.savefig(config["output_plot_path"]+"CDF_Rentals_Distance.pdf", bbox_inches="tight")
