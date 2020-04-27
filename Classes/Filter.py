import pandas as pd

class Filter:

    def __init__(self, df, config):
        self.df=df
        self.config = config

    def remove_fake_bookings(self):
        df = self.df
        config = self.config
        df = df[(df['start_lon'] >= config["TO_min_lon"]) & (df['start_lon'] <= config["TO_max_lon"])]
        df = df[(df['start_lat'] >= config["TO_min_lat"]) & (df['start_lon'] <= config["TO_max_lat"])]
        df = df[(df['end_lon'] >= config["TO_min_lon"]) & (df['end_lon'] <= config["TO_max_lon"])]
        df = df[(df['end_lat'] >= config["TO_min_lat"]) & (df['end_lon'] <= config["TO_max_lat"])]

        return df


    def split_df(self, is_rental=True):
        df = self.df
        config = self.config
        if is_rental == True:
            df = df[df['distance'] >= config["distance_m_min"]]
            df = df[(df['duration'] >= config["duration_s_min"]) & (df['duration'] <= config["duration_s_max"])]
        else:
            df = df[df['distance'] == 0]
            df = df[(df['duration'] <= 60 * 30)]
        df_we = df[df.Wod.isin(["Saturday", "Sunday"])]
        df_wd = df[~df.Wod.isin(["Saturday", "Sunday"])]

        return {"df_we":df_we, "df_wd":df_wd}
