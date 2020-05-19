import sys
sys.path.append('../..')
from Classes.ReadConfig import ReadConfig
from Classes.Filter import Filter


import pandas as pd
import json
import matplotlib.pyplot as plt

class RentalBookingsPerHour:

    def __init__(self, config, df, labels=['car2go', 'enjoy'], agg_func='count', save=False, name='ReB_Hour.pdf', ):

        fig, ax = plt.subplots(1, 1, figsize=config['figsize'])

        for label in labels:
            sub_df = df[df.vendor == label]
            sub_df_filter = Filter(sub_df, config)
            sub_df_split_dict = sub_df_filter.split_WD_WE()
            sub_df_we = sub_df_split_dict['df_we']
            sub_df_wd = sub_df_split_dict['df_wd']
            column_ref = df.columns[0]
            # c2g_number_of_workingdays = c2g_wd.groupby('Wod').count()[column_ref].sum()
            # c2g_number_of_weekends = c2g_we.groupby('Wod').count()[column_ref].sum()


            sub_df_we = sub_df_we.groupby('Hour')[column_ref].agg(agg_func)
            sub_df_wd = sub_df_wd.groupby('Hour')[column_ref].agg(agg_func)

            ax.plot(sub_df_wd.index, sub_df_wd.values, color=config['colors_per_city'][label], label='%s Working Days' % label)
            ax.plot(sub_df_we.index, sub_df_we.values, color=config['colors_per_city'][label], label='%s Week Ends' % label, linestyle='--')

        ax.tick_params(axis='x', rotation=15)
        ax.legend()
        ax.set_xticks(range(0, 24))
        ax.grid()
        # ax.set_ylim(0,6000)

        if save:
            plt.savefig(config['output_plot_path'] + 'ReB_Hour.pdf', bboxinches='tight')
        fig.show()

