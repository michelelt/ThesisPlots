import sys
sys.path.append('../..')
import pandas as pd
import matplotlib.pyplot as plt

# if __name__=='__main__':
#     rc = ReadConfig('../config.json')
#     config = rc.get_config()
#     plt.rcParams.update({'font.size': config['fs']})
#
#     city = 'Torino'
#     provider = 'car2go'
#     nrows = 1000
#     label_x = 'duration'
#     # label_y = 'pt_duration'
#     label_y = 'driving_duration'
#
#     df = Loader(config, city, provider, nrows)
#
#     df_before_filters = df.copy()
#
#     filter = Filter(df, config)
#     filter.remove_fake_bookings_torino()
#     filter.date_standardization()
#     filter.rentals()

class HeatmapL1vsL2:

    def __init__(self, config, rental, label_x, label_y, save=False):
        df = rental
        provider = df.iloc[0]['vendor']

        df = df[df[label_y]!= -1]
        df[label_x] = df[label_x].div(60).astype(int)
        df[label_y] = df[label_y].div(60).astype(int)
        df = df.groupby([label_x, label_y]).count()['_id'].to_frame()

        pivot = pd.pivot_table(df, index=label_x, columns=label_y, values='_id', fill_value=0)
        complete_pivot= pd.DataFrame(index=range(0,61), columns=range(0,61), data=0)
        pivot = complete_pivot+pivot
        pivot = pivot.fillna(0)

        fig, ax = plt.subplots()
        im = ax.imshow(pivot, cmap='Reds')

        ax.invert_yaxis()
        ax.plot([0, 50], [0, 50], linestyle='--')
        ax.set_xlim([0, 50])
        ax.set_ylim([0, 50])
        ax.set_xlabel(label_y)
        ax.set_ylabel(label_x)

        fig.colorbar(im)
        fig.tight_layout()
        if save:
            plt.savefig(config['output_plot_path']+'%s_%s_vs_%s.pdf'%(provider, label_x, label_y))


        fig.show()
