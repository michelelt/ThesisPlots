import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../..')
from Classes.ReadConfig import ReadConfig
from Classes.Filter import Filter


def compute_cdf(y_set):
    values = y_set
    sorted_data = np.sort(values)
    yvals = np.arange(len(values)) / float(len(values) - 1)
    return sorted_data, yvals

def cdf_bookings_duration(c2g_b_we, c2g_b_wd, enj_b_we, enj_b_wd):
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
    fig.show()

def cdf_rental_duration(c2g_r_we, c2g_r_wd, enj_r_we, enj_r_wd):
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
    fig.show()

def cdf_rental_distance(c2g_r_we, c2g_r_wd, enj_r_we, enj_r_wd):
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
    fig.show()

def cdf_booking_duration_vs_google_duration(c2g, enj):
    '''
    CDF Booking Duration vs Driving Duration
    '''
    c2g = c2g[(c2g['driving_duration'] != -1) & (c2g['driving_duration'] > c2g['duration'])]
    c2g['faster_diff'] = c2g['driving_duration'].div(60) - c2g['duration'].div(60)
    enj = enj[(enj['driving_duration'] != -1) & (enj['driving_duration'] > enj['duration'])]
    enj['faster_diff'] = enj['driving_duration'].div(60) - enj['duration'].div(60)
    c2g_x, c2g_y = compute_cdf(c2g.faster_diff)
    enj_x, enj_y = compute_cdf(enj.faster_diff)

    fig,ax = plt.subplots(1,1, figsize=(16,9))
    ax.plot(c2g_x, c2g_y, color='blue', label='Car2go')
    ax.plot(enj_x, enj_y, color='red', label='Enjoy')
    ax.legend()
    ax.grid()
    ax.legend()
    ax.set_xlabel('Faster [min]')
    ax.set_ylabel('ECDF')
    plt.savefig(config["output_plot_path"] + "CDF_driving_vs_google_pt.pdf", bbox_inches="tight")
    fig.show()


if __name__ == '__main__':
    rc = ReadConfig('../config.json')
    config = rc.get_config()
    plt.rcParams.update({'font.size': config['fs']})

    nrows=100000

    c2g = pd.read_csv(config['data_path']+'Torino.csv', nrows=nrows)
    c2g_filter = Filter(c2g, config)
    c2g_filter.remove_fake_bookings_torino()
    c2g_filter.date_standardization()
    out_b = c2g_filter.split_WD_WE()
    c2g_b_we = out_b['df_we']
    c2g_b_wd = out_b['df_wd']
    c2g_filter.rentals()
    out_r = c2g_filter.split_WD_WE()
    c2g_r_we = out_r['df_we']
    c2g_r_wd = out_r['df_wd']

    enj = pd.read_csv(config['data_path'] + 'enjoyTorino.csv', nrows=nrows)
    enj_filter = Filter(enj, config)
    enj_filter.remove_fake_bookings_torino()
    enj_filter.date_standardization()
    out_b = enj_filter.split_WD_WE()
    enj_b_we = out_b['df_we']
    enj_b_wd = out_b['df_wd']
    enj_filter.rentals()
    out_r = enj_filter.split_WD_WE()
    enj_r_we = out_r['df_we']
    enj_r_wd = out_r['df_wd']


    # TODO: Check something on booking durations
    cdf_bookings_duration(c2g_b_we, c2g_b_wd, enj_b_we, enj_b_wd)
    cdf_rental_duration(c2g_r_we, c2g_r_wd, enj_r_we, enj_r_wd)
    cdf_rental_distance(c2g_r_we, c2g_r_wd, enj_r_we, enj_r_wd)
    #
    cdf_booking_duration_vs_google_duration(c2g, enj)
