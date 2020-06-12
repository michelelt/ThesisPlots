import pandas as pd

class Filter:

    def __init__(self, df, config):
        self.df=df
        self.config = config
        self.itz = None
        self.ttz = None

    def date_standardization(self, fmt='%Y-%m-%d %H:%M:%S'):
        df = self.df
        print(df.vendor[0], df.init_date[0], fmt)
        df['Date_index'] = pd.to_datetime(df.init_date, format=fmt)
        df['Wod'] = df.Date_index.dt.day_name()
        df['Hour'] = df.Date_index.dt.hour
        df['Date'] = df.Date_index.dt.date
        self.df=df
        return  df

    def localize_timezone(self, column, itz, ttz):
        df = self.df
        df[column] = df[column].dt.tz_localize(itz).dt.tz_convert(ttz)
        df['Hour'] = df.Date_index.dt.hour
        self.itz = itz
        self.ttz = ttz
        self.df=df
        return df


    def remove_fake_bookings_torino(self):
        df = self.df
        config = self.config
        df = df[(df['start_lon'] >= config["TO_min_lon"]) & (df['start_lon'] <= config["TO_max_lon"])]
        df = df[(df['start_lat'] >= config["TO_min_lat"]) & (df['start_lon'] <= config["TO_max_lat"])]
        df = df[(df['end_lon'] >= config["TO_min_lon"]) & (df['end_lon'] <= config["TO_max_lon"])]
        df = df[(df['end_lat'] >= config["TO_min_lat"]) & (df['end_lon'] <= config["TO_max_lat"])]
        self.df = df
        return df

    def remove_fake_bookings_minneapolis(self):
        df = self.df
        config = self.config
        df = df[(df['start_lon'] >= config["Minn_min_lon"]) & (df['start_lon'] <= config["Minn_max_lon"])]
        df = df[(df['start_lat'] >= config["Minn_min_lat"]) & (df['start_lon'] <= config["Minn_max_lat"])]
        df = df[(df['end_lon'] >= config["Minn_min_lon"]) & (df['end_lon'] <= config["Minn_max_lon"])]
        df = df[(df['end_lat'] >= config["Minn_min_lat"]) & (df['end_lon'] <= config["Minn_max_lat"])]
        self.df = df
        return df

    def split_WD_WE(self):
        df = self.df

        df_we = df[df.Wod.isin(["Saturday", "Sunday"])]
        df_wd = df[~df.Wod.isin(["Saturday", "Sunday"])]

        return {"WE": df_we, "WD": df_wd}


    def reservation(self, provider):
        df = self.df
        if provider =='car2go':
            df = df[df['distance'] == 0]
            df = df[(df['duration'] <= 60 * 20)]
        elif provider == 'enjoy':
            df = df[df['distance'] == 0]
            df = df[(df['duration'] <= 60 * 15)]
        else:
            print('Wrong provider')
            return
        self.df = df
        return df

    def rentals(self):
        df = self.df
        config = self.config
        df = df[(df['distance'] >= config["distance_m_min"]) & (df['distance'] <= config["distance_m_max"]) ]
        df = df[(df['duration'] >= config["duration_s_min"]) & (df['duration'] <= config["duration_s_max"])]
        self.df = df
        return df

    def limit_date(self):
        df = self.df
        config = self.config
        if self.ttz != None:
            lowerbound_date = config['init_date'].tz_localize(self.ttz)
            upperbound_date = config['final_date'].tz_localize(self.ttz)
        else:
            lowerbound_date = config['init_date']
            upperbound_date = config['final_date']

        df = df[(df['Date_index'] >= lowerbound_date) & (df['Date_index'] <= upperbound_date)]
        self.df = df
        return df

