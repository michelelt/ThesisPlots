import pandas as pd
import json
import datetime


class Car2goFormatter:

    def __init__(self, df):
        self.df = df
        self.format_df(df)

    def format_df(self, df):
        if 'driving' in df.columns:
            def f(line):
                line = str(line)
                line = line.replace('\'', '\"')
                line_dict = json.loads(line)
                return line_dict['duration'], line_dict['distance']

            df[['driving_duration', 'driving_distance']] = df.apply(lambda x: f(x.driving), axis=1, result_type='expand')
            df = df.drop('driving', axis=1)


        if 'origin_destination' in df.columns:
            def f(line):
                line = str(line)
                line = line.replace('\'', '\"')
                line_dict = json.loads(line)
                return line_dict['coordinates'][0][0],\
                       line_dict['coordinates'][0][1],\
                       line_dict['coordinates'][1][0],\
                       line_dict['coordinates'][1][1]

            df[['start_lon', 'start_lat', 'end_lon', 'end_lat']] = df.apply(lambda x: f(x.origin_destination), axis=1, result_type='expand')
            df = df.drop('origin_destination', axis=1)

        if 'public_transport' in df.columns:
            def f(line):
                line = str(line)
                line = line.replace('\'', '"')
                line = line.replace('datetime.datetime(', '"datetime.datetime(')
                line = line.replace(')', ')"')
                line_dict = json.loads(line)
                line_dict['arrival_ts'] = -1

                if line_dict['arrival_date'] != -1:
                    date_list = line_dict['arrival_date'].replace('datetime.datetime(', '').replace(')', '')
                    dt = date_list.split(', ')
                    dt = [int(x) for x in dt]
                    try:
                        line_dict['arrival_date'] = datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
                    except IndexError:
                        line_dict['arrival_date'] = datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4], 0)
                        line_dict['arrival_ts'] = datetime.datetime.timestamp(
                            datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4], 0)
                        )

                return line_dict['arrival_time'],\
                       line_dict['duration'],\
                       line_dict['arrival_date'],\
                       line_dict['arrival_ts'],\
                       line_dict['distance']

            df[['pt_arrival_time', 'pt_duration', 'pt_arrival_date','pt_arrival_time', 'pt_distance']] =\
                df.apply(lambda x: f(x.public_transport), axis=1, result_type='expand')
            df = df.drop('public_transport', axis=1)


        if 'walking' in df.columns:
            def f(line):
                line = str(line)
                line = line.replace('\'', '\"')
                line_dict = json.loads(line)
                return line_dict['duration'],\
                       line_dict['distance']


            df[['walking_duration', 'walking_distance']] = df.apply(lambda x: f(x.walking), axis=1, result_type='expand')
            df = df.drop('walking', axis=1)

        self.df = df

    def get_df(self):
        return self.df


