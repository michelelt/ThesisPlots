import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import time


class DF2GDF:
    def __init__(self): pass

    def df2gdf_point(self, df, columns, crs):
        print('-->', columns)
        geometry = [Point(xy) for xy in zip(df[columns["Lon"]], df[columns["Lat"]])]
        gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

        return gdf

    def assign_zone_to_rental(self, df_start, df_end, map, convert_dict_start={}, convert_dict_end={}):
        df = df_start.copy()
        df = df.drop('geometry',axis=1)


        print('Begin of START point ad zones')
        start = time.time()
        df_start = gpd.sjoin(df_start, map, how='inner', op='within')
        df_start = df_start.rename(columns=convert_dict_start)
        print('End of START point ad zones in %.2f' % (time.time()-start))

        print('Begin of END point ad zones')
        start = time.time()
        df_end = gpd.sjoin(df_end, map, how='inner', op='within')
        df_end = df_end.rename(columns=convert_dict_end)
        print('End of END point ad zones in %.2f' % (time.time()-start))


        df[list(convert_dict_start.values())] = df_start[list(convert_dict_start.values())]
        df[list(convert_dict_end.values())] = df_end[list(convert_dict_end.values())]

        return df

    def dump_df(self, df, name, path):
        df.to_csv(path+name+'_with_zone_ID.csv', index=False)

    def drop_zones_without_bookings(self, df, map):
        start_zones = list(df.start_zone_ID.unique())
        end_zones = list(df.end_zone_ID.unique())
        zones_set = set(start_zones+end_zones)
        map = map.loc[zones_set]
        return map


    def reshape_caselle(self, map, index):
        if index in map.index:
            a = [7.62, 45.128]
            b = [7.63, 45.128]
            c = [7.63, 45.132]
            d = [7.62, 45.132]
            point_list=[a,b,c,d]

            new_caselle = Polygon(point_list)

            map.loc[index,'geometry'] = new_caselle
        return map






