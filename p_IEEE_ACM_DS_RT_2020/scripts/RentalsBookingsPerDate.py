import sys
sys.path.append('../..')
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt

class RentalsBookingsPerDate:

    def __init__(self,config, bookings, rentals, labels, save=False, name='ReB_date.pdf'):
        try:
            min_date = bookings.Date.min()
            max_date = bookings.Date.max()
            ref_col = bookings.columns[0]

        except AttributeError:
            min_date = rentals.Date.min()
            max_date = rentals.Date.max()
            ref_col = rentals.columns[0]

        date_list = pd.DataFrame(pd.date_range(min_date, max_date), columns=['Date_list'])
        date_list['Date_list'] = pd.to_datetime(date_list['Date_list'])
        date_list['Date_list'] = date_list.Date_list.dt.date


        fig, ax = plt.subplots(1, 1, figsize=config['figsize'])
        for label in labels:
            if isinstance(bookings, pd.DataFrame):
                df_b = bookings[bookings.vendor == label]
                df_b = df_b.groupby('Date').count().sort_index()
                df_b = date_list.merge(df_b, how='left', left_on='Date_list', right_index=True).set_index('Date_list')[ref_col]
                ax.plot(df_b.index, df_b.values, color=config['colors_per_city'][label], label='%s Bookings' %label)
                print(label, 'bookings', df_b.shape)
                self.df_b = df_b

            if isinstance(rentals, pd.DataFrame):
                df_r = rentals[rentals.vendor == label]
                df_r = df_r.groupby('Date').count().sort_index()
                df_r = date_list.merge(df_r, how='left', left_on='Date_list', right_index=True).set_index('Date_list')[ref_col]
                ax.plot(df_r.index, df_r.values, color=config['colors_per_city'][label], label='%s Rentals' %label)
                print(label, 'rentalss', df_r.shape)
                self.df_r = df_r

        monthyearFmt = mdates.DateFormatter('%b \'%y')
        ax.xaxis.set_major_formatter(monthyearFmt)
        ax.tick_params(axis='x', rotation=15)
        ax.legend()
        ax.grid()
        ax.set_ylabel('Rentals per day')
        ax.set_xlabel('Date')
        if save:
            plt.savefig(config['output_plot_path'] + name, bboxinches='tight')

        fig.show()

    def get_df_br(self):
        return self.df_b, self.df_r


