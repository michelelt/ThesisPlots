import sys
sys.path.append('../..')
from Classes.Filter import Filter
from Classes.Loader import Loader


import pandas as pd
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    with open('../config.json') as fp: config = json.load(fp)
    plt.rcParams.update({'font.size': config['fs']})

    nrows=100000
    provider = 'both'
    city = 'Torino'
    label_x = 'duration'
    label_y = 'pt_duration'

    df = Loader(config, city, provider, nrows)
    filter = Filter(df, config)
    filter.date_standardization()
    filter.remove_fake_bookings_torino()
    filter.rentals()

    df = df[df['pt_duration'] > -1]
    len_c2g = df[df['vendor'] == 'car2go'].shape[0]
    len_enj = df[df['vendor'] == 'enjoy'].shape[0]
    df['TimeBin'] = df['pt_duration'].div(60).div(5).astype(int)
    indeces = df[df['TimeBin'] >=10].index
    df.loc[indeces, 'TimeBin'] = 10

    df = df.groupby(['vendor', 'TimeBin']).count()['_id'].reset_index()
    car2go = df[df['vendor'] =='car2go'].set_index('TimeBin')
    enjoy = df[df['vendor'] == 'enjoy'].set_index('TimeBin')


    labels=['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35',
            '35-40','40-45', '45-50', '50+']
    x = df.TimeBin.unique()
    width=0.35


    fig, ax = plt.subplots(figsize=config['figsize'])
    ax.bar(x - width/2, car2go['_id'].div(len_c2g).mul(100), width, label='car2go', color='blue')
    ax.bar(x + width/2, enjoy['_id'].div(len_enj).mul(100), width, label='enjoy', color='red')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, fontsize=config['fs'])
    ax.legend(fontsize=config['fs'])
    ax.set_yticklabels(range(0,20,2), fontsize=config['fs'])
    ax.grid()

    ax.set_xlabel('Public transportation time [min]')
    ax.set_ylabel('Booking probability [%]')

    plt.savefig(config['output_plot_path']+'pt_chose_probability.pdf', bbox_inches='tight')
    fig.show()







    
