import sys
sys.path.append('../..')
from Classes.Filter import Filter
from Classes.DF2GDF import DF2GDF


import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt

def print_line(df, index):
    print(df.iloc[index]['start_lat'], df.iloc[index]['end_lat'])

def print_point(df1, df2, index):
    print(str(df1.geometry.iloc[index]), (str(df1.start_lon.iloc[index]), str(df1.start_lat.iloc[index]) ))
    print(str(df2.geometry.iloc[index]), (str(df2.end_lon.iloc[index]), str(df2.end_lat.iloc[index]) ))
    print()



if __name__=='__main__':
    with open('../config.json') as fp : config = json.load(fp)
    nrows = None
    provider = 'car2go'

    if provider == 'car2go': df = pd.read_csv(config['data_path'] + 'Torino.csv', nrows=nrows)
    else: df = pd.read_csv(config['data_path'] + 'enjoyTorino.csv', nrows=nrows)

    filter = Filter(df, config)
    df = filter.remove_fake_bookings()
    df['Date_index'] = pd.to_datetime(df.init_date, format='%Y-%m-%d %H:%M:%S')
    df['Date'] = df.Date_index.dt.date
    df["Wod"] = df.Date_index.dt.weekday_name

    converter = DF2GDF()
    df_start = converter.df2gdf_point(df.copy(), dict(Lon='start_lon', Lat='start_lat'), crs=config['crs'])
    df_end = converter.df2gdf_point(df.copy(), dict(Lon='end_lon', Lat='end_lat'), crs=config['crs'])
    city_map = gpd.read_file(config['data_path']+'TorinoShape/Zonizzazione.shp')[['zone_name', 'geometry']]
    city_map = city_map.to_crs(config['crs'])

    df = converter.assign_zone_to_rental(df_start, df_end, city_map,
                                         convert_dict_start={'index_right': 'start_zone_ID', 'zone_name': 'start_zone_name'},
                                         convert_dict_end={'index_right': 'end_zone_ID', 'zone_name': 'end_zone_name'})
    converter.dump_df(df, provider+'Torino', config['data_path'])

    city_map_cleaned = converter.drop_zones_without_bookings(df, city_map)

    '''Morning bookings'''
    df['Hour'] = df.Hour.astype(int)
    df_m = df[df.Hour.isin(list(range(7, 13)))]
    df_m = df_m.groupby('end_zone_ID').count()['_id']

    '''Evening'''
    df_e = df[df.Hour.isin(list(range(17, 22)))]
    df_e = df_e.groupby('end_zone_ID').count()['_id']

    city_map_cleaned['actract'] = df_e - df_m
    city_map_cleaned = converter.reshape_caselle(city_map_cleaned, config['caselleID'])
    city_map_cleaned = city_map_cleaned.dropna()


    fig, ax = plt.subplots()
    city_map_cleaned.plot(ax=ax, column='actract',  legend=True)
    plt.savefig(config['output_plot_path']+provider+'Torino.pdf')






