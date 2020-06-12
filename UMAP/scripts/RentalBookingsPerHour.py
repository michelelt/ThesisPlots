import sys
sys.path.append('../..')
from Classes.Filter import Filter
import matplotlib.pyplot as plt


class RentalBookingsPerHour:

    def __init__(self, config, df, labels=['car2go', 'enjoy'], agg_func='count', save=False,
                 norm_per_day=False, name='ReB_Hour.pdf', ):


        fig, ax = plt.subplots(1, 1, figsize=config['figsize'])

        for label in labels:
            sub_df = df[df.vendor == label]
            sub_df_filter = Filter(sub_df, config)
            sub_df_split_dict = sub_df_filter.split_WD_WE()
            sub_df_we = sub_df_split_dict['WE']
            sub_df_wd = sub_df_split_dict['WD']


            if agg_func == 'count':
                sub_df_we = sub_df_we.groupby('Hour').count()
                sub_df_wd = sub_df_wd.groupby('Hour').count()
            elif agg_func == 'mean':
                sub_df_we = sub_df_we.groupby('Hour').mean()
                sub_df_wd = sub_df_wd.groupby('Hour').mean()
            else:
                print('error')
                return

            sub_df_we = sub_df_we.div(self.compute_number_of_days(sub_df_we, norm_per_day))
            sub_df_wd = sub_df_wd.div(self.compute_number_of_days(sub_df_we, norm_per_day))

            columns_ref = sub_df_we.columns[0]
            sub_df_we = sub_df_we[columns_ref]
            sub_df_wd = sub_df_wd[columns_ref]
            ax.plot(sub_df_wd.index, sub_df_wd.values, color=config['colors'][label], label='%s Working Days' % label)
            ax.plot(sub_df_we.index, sub_df_we.values, color=config['colors'][label], label='%s Week Ends' % label, linestyle='--')

        ax.tick_params(axis='x', rotation=15)
        ax.legend()
        ax.set_xticks(range(0, 24))
        ax.grid()
        # ax.set_ylim(0,6000)
        ax.set_ylabel('Rentals per hour')
        ax.set_xlabel('Hour of day')

        if save:
            plt.savefig(config['output_plot_path'] + name, bboxinches='tight')
        fig.show()


    def compute_number_of_days(self, df, norm_per_day):
        if norm_per_day == True:
            return len(df.Date.unique())
        else:
            return 1


