import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../..')
from Classes.ReadConfig import ReadConfig
from Classes.Filter import Filter

class CDFs :
    def __init__(self, config, df, labels=['car2go', 'enjoy']):
        self.df = df
        self.config = config

        self.datasets={}

        for label in labels:
            sub_df = self.df[df.vendor==label]
            self.datasets[label]={}
            self.datasets[label]['bookings'] = {}
            self.datasets[label]['rentals '] = {}

            filter = Filter(sub_df, config)
            out_b = filter.split_WD_WE()
            self.datasets[label]['bookings'] = out_b
            filter.rentals()
            out_r = filter.split_WD_WE()
            self.datasets[label]['rentals'] = out_r
        self.labels = labels


    def compute_cdf(self, y_set):
        values = y_set
        sorted_data = np.sort(values)
        yvals = np.arange(len(values)) / float(len(values) - 1)
        return sorted_data, yvals


    def saveplot(self, save, name):
        if save: plt.savefig(self.config["output_plot_path"] + name, bbox_inches="tight")



    def cdf_bookings_duration(self, save=False, name="CDF_Bookings_Duration.pdf"):
        '''
        cdf BOOKINGS DURATION -> does not produce a rental
        '''

        fig,ax = plt.subplots(1,1, figsize=self.config['figsize'])
        for label in self.labels:
            x_b_we, y_b_we = self.compute_cdf(self.datasets[label]['bookings']['WE'].duration.div(60))
            x_b_wd, y_b_b_wd = self.compute_cdf(self.datasets[label]['bookings']['WD'].duration.div(60))
            ax.plot(x_b_we, y_b_we, color=self.config['colors_per_city'][label], label='%s Week Days' %label)
            ax.plot(x_b_wd, y_b_b_wd, color=self.config['colors_per_city'][label], linestyle='--', label="%s Week Ends"% label)


        ax.grid()
        ax.legend()
        # ax.set_xticks(range(0, 1801, 5*60))
        # ax.set_xticklabels(range(0,31, 5))
        ax.set_xlabel("Duration [min]")
        ax.set_ylabel("ECDF")
        self.saveplot(save, name)
        fig.show()

    def cdf_rental_duration(self, save=False, name="CDF_Rentals_Duration.pdf"):
        '''
        cdf RENTAL DURATION
        '''
        fig,ax = plt.subplots(1,1, figsize=self.config['figsize'])
        for label in self.labels:
            x_b_we, y_b_we = self.compute_cdf(self.datasets[label]['rentals']['WE'].duration.div(60))
            x_b_wd, y_b_b_wd = self.compute_cdf(self.datasets[label]['rentals']['WD'].duration.div(60))
            ax.plot(x_b_we, y_b_we, color=self.config['colors_per_city'][label], label='%s Week Days' %label)
            ax.plot(x_b_wd, y_b_b_wd, color=self.config['colors_per_city'][label], linestyle='--', label="%s Week Ends"% label)


        ax.grid()
        ax.legend()
        # ax.set_xticks(range(0, 1801, 5*60))
        # ax.set_xticklabels(range(0,31, 5))
        ax.set_xlabel("Duration [min]")
        ax.set_ylabel("ECDF")
        self.saveplot(save, name)
        fig.show()

    def cdf_rental_distance(self, save=False, name="CDF_Rentals_Distance.pdf"):
        '''
        cdf RENTAL DISTANCE
        '''

        fig,ax = plt.subplots(1,1, figsize=self.config['figsize'])
        for label in self.labels:
            x_b_we, y_b_we = self.compute_cdf(self.datasets[label]['rentals']['WE'].distance.div(1000))
            x_b_wd, y_b_b_wd = self.compute_cdf(self.datasets[label]['rentals']['WD'].distance.div(1000))
            ax.plot(x_b_we, y_b_we, color=self.config['colors_per_city'][label], label='%s Week Days' %label)
            ax.plot(x_b_wd, y_b_b_wd, color=self.config['colors_per_city'][label], linestyle='--', label="%s Week Ends"% label)


        ax.grid()
        ax.legend()
        ax.set_xlabel("Distance [km]")
        ax.set_ylabel("ECDF")
        self.saveplot(save, name)
        fig.show()

    def cdf_booking_duration_vs_google_duration(self, save=False, name="CDF_driving_vs_google_pt.pdf"):
        '''
        CDF Booking Duration vs Driving Duration
        '''

        c2g = self.c2g[(self.c2g['driving_duration'] != -1) & (self.c2g['driving_duration'] > self.c2g['duration'])]
        c2g['faster_diff'] = c2g['driving_duration'].div(60) - c2g['duration'].div(60)
        enj = self.enj[(self.enj['driving_duration'] != -1) & (self.enj['driving_duration'] > self.enj['duration'])]
        enj['faster_diff'] = enj['driving_duration'].div(60) - enj['duration'].div(60)
        c2g_x, c2g_y = self.compute_cdf(c2g.faster_diff)
        enj_x, enj_y = self.compute_cdf(enj.faster_diff)

        fig,ax = plt.subplots(1,1,  figsize=self.config['figsize'])
        ax.plot(c2g_x, c2g_y, color='blue', label='Car2go')
        ax.plot(enj_x, enj_y, color='red', label='Enjoy')
        ax.legend()
        ax.grid()
        ax.legend()
        ax.set_xlabel('Faster [min]')
        ax.set_ylabel('ECDF')
        self.saveplot(save, name)
        fig.show()



