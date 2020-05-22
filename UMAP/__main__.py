import sys
sys.path.append('..')
sys.path.append('./scripts')

from Classes.Loader import Loader
from Classes.Filter import Filter
from Classes.ReadConfig import ReadConfig
from Classes.Filter import Filter

from scripts.CDFs import CDFs

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

if __name__ == '__main__':
    nrows = 10000
    config = ReadConfig('config.json')
    plt.rcParams.update({'font.size': config['fs']})

    c2g = Loader(config, 'Torino', 'car2go', nrows)
    c2g_filter = Filter(c2g , config)
    c2g_filter.date_standardization(fmt='%Y-%m-%d %H:%M:%S')
    c2g_allevents = c2g.copy()
    c2g['Date'] = c2g.Date_index.dt.date
    c2g['Date'] = c2g.Date_index.dt.date

    enj = Loader(config, 'Torino', 'enjoy', nrows)
    enj_filter = Filter(enj, config)
    enj_filter.date_standardization(fmt='%Y-%m-%d %H:%M:%S')
    enj_allevents = enj.copy()
    enj['Date'] = enj.Date_index.dt.date
    enj_allevents['Date'] = enj_allevents.Date_index.dt.date
    #

    df_allevents = c2g_allevents.append(enj_allevents, sort=False)
    df = c2g.append(enj, sort=False)

    # cdfs = CDFs(config, df)
    # cdfs.cdf_bookings_duration(save=False)
    # cdfs.cdf_rental_duration(save=False)
    # cdfs.cdf_rental_distance(save=False)
    # cdfs.cdf_booking_duration_vs_google_duration(save=False)
