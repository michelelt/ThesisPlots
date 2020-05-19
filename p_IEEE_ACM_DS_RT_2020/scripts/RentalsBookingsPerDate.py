import sys
sys.path.append('../..')
from Classes.ReadConfig import ReadConfig

import pandas as pd
import json
import matplotlib.pyplot as plt

class RentalsBookingsPerDate:

    def __init__(self,config, bookings, rentals, labels, save=False, name='ReB_date.pdf'):

        min_date = bookings.Date.min()
        max_date = bookings.Date.max()

        date_list = pd.DataFrame(pd.date_range(min_date, max_date), columns=['Date_list'])
        date_list['Date_list'] = pd.to_datetime(date_list['Date_list'])
        date_list['Date_list'] = date_list.Date_list.dt.date

        ref_col_b = bookings.columns[0]
        ref_col_r = bookings.columns[0]

        fig, ax = plt.subplots(1, 1, figsize=config['figsize'])
        for label in labels:
            df_b = bookings[bookings.vendor == label]
            df_b['Date'] = df_b.Date_index.dt.date
            df_r = rentals[rentals.vendor == label]
            df_r['Date'] = df_r.Date_index.dt.date
            df_b = df_b.groupby('Date').count().sort_index()
            df_r = df_r.groupby('Date').count().sort_index()



            df_b = date_list.merge(df_b, how='left', left_on='Date_list', right_index=True).set_index('Date_list')[ref_col_b]
            df_r = date_list.merge(df_r, how='left', left_on='Date_list', right_index=True).set_index('Date_list')[ref_col_r]

            date_labels = pd.to_datetime(date_list['Date_list']).dt. \
                strftime('%b \'%y').drop_duplicates().reset_index().drop('index', axis=1)


            ax.plot(df_b.index, df_b.values, color=config['colors_per_city'][label], label='%s Bookings' %label)
            ax.plot(df_r.index, df_r.values, color=config['colors_per_city'][label], label='%s Rentals' %label, linestyle='--')

        # ax.set_xticks(date_labels.index)
        ax.set_xticklabels(date_labels.Date_list.tolist())
        ax.tick_params(axis='x', rotation=15)
        ax.legend()
        ax.grid()
        if save:
            plt.savefig(config['output_plot_path'] + name, bboxinches='tight')

        fig.show()




