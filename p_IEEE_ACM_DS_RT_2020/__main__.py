import sys
sys.path.append('..')
sys.path.append('./scripts')

from Classes.Loader import Loader
from Classes.Filter import Filter
from Classes.ReadConfig import ReadConfig
from Classes.Filter import Filter

from scripts.CDFs import CDFs
from scripts.RentalsBookingsPerDate import RentalsBookingsPerDate
from scripts.RentalBookingsPerHour import RentalBookingsPerHour

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

new_columns={'TripDuration':'duration', 'TripDistance':'distance', 'StartTime':'init_date', 'EndTime':'final_date'}


def get_df_br():
    zz1, zz2 = RentalBookingsPerHour.get_df_br()


if __name__ == '__main__':
    l1 = 'Minneapolis'
    l2 = 'Louisville'
    nrows = None
    config = ReadConfig('config.json')
    plt.rcParams.update({'font.size': config['fs']})



    minn = Loader(config, l1, 'car2go', nrows)
    minn['vendor'] = 'Minneapolis'
    minn = minn.rename(columns=new_columns)

    not_formatted_init = minn[minn.init_date.str.contains('/')].index
    minn.loc[not_formatted_init,'init_date'] = minn.init_date.str.replace('/','-').str.replace(' ', 'T')
    minn.loc[not_formatted_init,'init_date'] = minn.loc[not_formatted_init,'init_date'] + '.000Z'

    not_formatted_final = minn[minn.final_date.str.contains('/')].index
    minn.loc[not_formatted_init,'final_date'] = minn.init_date.str.replace('/','-').str.replace(' ', 'T')
    minn.loc[not_formatted_init,'final_date'] = minn.loc[not_formatted_init,'final_date'] + '.000Z'

    minn_filter = Filter(minn, config)
    minn_filter.date_standardization(fmt='%Y-%m-%dT%H:%M:%S.000Z')
    minn_filter.localize_timezone('Date_index', 'UTC', 'America/Chicago')
    minn_filter.limit_date()

    minn_allevents = minn.copy()
    minn = minn_filter.df
    minn['Date'] = minn.Date_index.dt.date
    minn_allevents['Date'] = minn_allevents.Date_index.dt.date


    louis = Loader(config, l2, 'car2go', nrows)
    louis = louis[~louis.StartTime.str.contains('24:')]
    louis['StartTime'] = louis['StartDate']+'T'+louis['StartTime']+':00.000Z'
    louis['vendor'] = 'Louisville'
    louis['TripDuration'] = louis['TripDuration'].mul(60)
    louis['TripDistance'] = louis['TripDistance'].mul(1000)
    louis = louis.rename(columns=new_columns)
    louis_filter = Filter(louis, config)
    louis_filter.date_standardization(fmt='%Y-%m-%dT%H:%M:%S.000Z')
    louis_filter.limit_date()

    louis_allevents = louis.copy()
    louis = louis_filter.df
    louis['Date'] = louis.Date_index.dt.date
    louis_allevents['Date'] = louis_allevents.Date_index.dt.date


    df_allevents = minn_allevents.append(louis_allevents, sort=False)
    df = minn.append(louis, sort=False)


    # cdfs = CDFs(config, df, labels=[l1, l2])
    # cdfs.cdf_rental_duration(save=True)
    # cdfs.cdf_rental_distance(save=True)

    RentalsBookingsPerDate(config, None, df, labels=[l1, l2], save=False)
    # RentalBookingsPerHour(config, df, labels=[l1, l2], norm_per_day=True, save=True)

