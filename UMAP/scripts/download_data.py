import sys
sys.path.append('..')

from Classes.DataDownloader import DataDownloader

import pandas as pd
import datetime

city = sys.argv[1]
for i in range(1, len(sys.argv)):

    city = sys.argv[i]
    # init_date = datetime.datetime(2017, 11, 1, 23, 59, 59)
    # final_date = datetime.datetime(2017, 11, 2, 23, 59, 59)
    init_date = None
    final_date = None
    print('Query on %s' % city)
    print('Init date', init_date)
    print('final date', final_date)
    data_downloader = DataDownloader(init_date, final_date)
    data_downloader.download_data(city)
    data_downloader.dump_df('../Data/', 'csv')

    if city == 'Torino':
        print('Enjoy')
        data_downloader.download_data(city, 'enjoy')
        data_downloader.dump_df('../Data/', 'csv')
    print()
