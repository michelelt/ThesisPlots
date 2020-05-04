import pandas as pd

class Filter:

    def __init__(self, df, config):
        self.df=df
        self.config = config

    def date_standardization(self):
        df = self.df
        df['Date_index'] = pd.to_datetime(df.init_date, format='%Y-%m-%d %H:%M:%S')
        df['Wod'] = df.Date_index.dt.weekday_name
        self.df=df
        return  df


    def remove_fake_bookings_torino(self):
        df = self.df
        config = self.config
        df = df[(df['start_lon'] >= config["TO_min_lon"]) & (df['start_lon'] <= config["TO_max_lon"])]
        df = df[(df['start_lat'] >= config["TO_min_lat"]) & (df['start_lon'] <= config["TO_max_lat"])]
        df = df[(df['end_lon'] >= config["TO_min_lon"]) & (df['end_lon'] <= config["TO_max_lon"])]
        df = df[(df['end_lat'] >= config["TO_min_lat"]) & (df['end_lon'] <= config["TO_max_lat"])]
        self.df = df
        return df

    def split_WD_WE(self):
        df = self.df

        df_we = df[df.Wod.isin(["Saturday", "Sunday"])]
        df_wd = df[~df.Wod.isin(["Saturday", "Sunday"])]

        return {"df_we": df_we, "df_wd": df_wd}


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
        df = df[df['distance'] >= config["distance_m_min"]]
        df = df[(df['duration'] >= config["duration_s_min"]) & (df['duration'] <= config["duration_s_max"])]
        self.df = df
        return df

    def limit_date(self):
        df = self.df
        config = self.config
        df = df[(df['init_time'] >= config["init_time"]) & (df['final_time'] <= config["final_time"])]
        self.df = df
        return df

