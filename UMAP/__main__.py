import sys
sys.path.append('..')
sys.path.append('./scripts')

from Classes.Loader import Loader
from Classes.Filter import Filter
from Classes.ReadConfig import ReadConfig
from Classes.Filter import Filter

from scripts.CDFs import CDFs
from scripts.RentalBookingsPerHour import RentalBookingsPerHour
from scripts.RentalBookingsPerDay import RentalBookingsPerDay
from scripts.HeatmapFlows import HeatmapFlows
from scripts.HeatmapL1vsL2 import HeatmapL1vsL2
from scripts.PTChoseProbability import PTChoseProbability
from scripts.AvgTimePerTransportSolution import AvgTimePerTransportSolution

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

if __name__ == '__main__':
    nrows = 120000
    config = ReadConfig('config.json')
    plt.rcParams.update({'font.size': config['fs']})

    col2keep = ['_id', 'city', 'distance', 'driving_distance', 'driving_duration', 'duration', 'end_lat', 'end_lon',
                'final_address', 'final_date', 'final_fuel', 'final_time', 'init_address', 'init_date', 'init_fuel',
                'init_time', 'plate', 'pt_arrival_date', 'pt_arrival_time', 'pt_distance',
                'pt_duration', 'start_lat', 'start_lon', 'vendor', 'walking_distance', 'walking_duration']

    c2g = Loader(config, 'Torino', 'car2go', nrows)
    c2g = c2g[col2keep]
    c2g_filter = Filter(c2g , config)
    c2g_filter.date_standardization(fmt='%Y-%m-%d %H:%M:%S')
    c2g_filter.remove_fake_bookings_torino()
    c2g_allevents = c2g.copy()
    c2g_filter.rentals()
    c2g = c2g_filter.df

    enj = Loader(config, 'Torino', 'enjoy', nrows)
    enj = enj[col2keep]
    enj_filter = Filter(enj, config)
    enj_filter.date_standardization(fmt='%Y-%m-%d %H:%M:%S')
    enj_filter.remove_fake_bookings_torino()
    enj_allevents = enj.copy()
    enj_filter.rentals()
    enj = enj_filter.df


    df_allevents = c2g_allevents.append(enj_allevents, sort=False, ignore_index=True)
    df = c2g.append(enj, sort=False, ignore_index=True)

    city_map = gpd.read_file(config['data_path'] + 'TorinoShape/Zonizzazione.shp')[['zone_name', 'geometry']]
    city_map = city_map.to_crs(config['crs'])

    q=0.9999
    subset = df[(df.pt_duration >-1) &
                          (df.driving_duration>-1)
                           ]
                          # (df.driving_duration <= df.driving_duration.quantile(q))]

    print(subset)

    # df_allevents.Date = df_allevents.Date_index.dt.date
    # RentalBookingsPerDay(config, df_allevents, df, save=True)
    #
    # RentalBookingsPerHour(config, df, save=True)
    #
    # cdfs = CDFs(config, df)
    # cdfs.cdf_bookings_duration(save=True)
    # cdfs.cdf_rental_duration(save=True)
    # cdfs.cdf_rental_distance(save=True)

    # HeatmapFlows(df, city_map, config, 'Torino', save=True)

    # HeatmapL1vsL2(config, df, 'duration', 'pt_duration', save=True)
    # HeatmapL1vsL2(config, df, 'duration', 'driving_duration', save=True)
    #
    # cdfs.cdf_booking_duration_vs_google_duration(save=True)
    #
    # PTChoseProbability(config, df, save=True)
    #
    AvgTimePerTransportSolution(config, df, save=False)



