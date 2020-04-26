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

