import sys
sys.path.append('../..')
from Classes.Filter import Filter
from Classes.DF2GDF import DF2GDF
from Classes.ReadConfig import ReadConfig
from Classes.Loader import Loader


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



class HeatmapFlows:
    def __init__(self, df, city_map, config, label, save=False):

        df_before_filters = df.copy()

        filter = Filter(df, config)
        filter.remove_fake_bookings_torino()
        filter.date_standardization()
        df = filter.rentals()

        converter = DF2GDF()
        df_start = converter.df2gdf_point(df.copy(), dict(Lon='start_lon', Lat='start_lat'), crs=config['crs'])
        df_end = converter.df2gdf_point(df.copy(), dict(Lon='end_lon', Lat='end_lat'), crs=config['crs'])

        df = converter.assign_zone_to_rental(df_start, df_end, city_map,
                                             convert_dict_start={'index_right': 'start_zone_ID', 'zone_name': 'start_zone_name'},
                                             convert_dict_end={'index_right': 'end_zone_ID', 'zone_name': 'end_zone_name'})
        df = df[df.start_zone_ID.notna()]
        df = df[df.end_zone_ID.notna()]

        converter.dump_df(df, label+'Torino', config['data_path'])

        city_map_cleaned = converter.drop_zones_without_bookings(df, city_map)

        '''Morning bookings'''
        df_m = df[df.Hour.isin(list(range(7, 13)))]
        df_m = df_m.groupby('end_zone_ID').count()['_id']

        '''Evening'''
        df_e = df[df.Hour.isin(list(range(17, 22)))]
        df_e = df_e.groupby('end_zone_ID').count()['_id']

        city_map_cleaned['actract'] = df_e - df_m
        city_map_cleaned = converter.reshape_caselle(city_map_cleaned, config['caselleID'])
        city_map_cleaned = city_map_cleaned.dropna()

        fig, ax = plt.subplots()
        city_map_cleaned.plot(ax=ax, column='actract', legend=True)
        ax.set_xticks([])
        ax.set_yticks([])

        if save: plt.savefig(config['output_plot_path']+label+'Torino.pdf')

        fig.show()






