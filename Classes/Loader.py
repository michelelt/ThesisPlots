import pandas as pd

class Loader:

    def __init__(self, config, city, provider, nrows):
        return


    def __new__(cls, config, city, provider, nrows):
        if provider == 'car2go':
            df = pd.read_csv(config['data_path'] + '%s.csv'%city, nrows=nrows)
        elif provider=='both':
            df=pd.read_csv(config['data_path'] + '%s.csv'%city, nrows=nrows)\
            .append(pd.read_csv(config['data_path'] + 'enjoy%s.csv'%city, nrows=nrows), ignore_index=True, sort=False)
        elif provider == 'enjoy':
            df = pd.read_csv(config['data_path'] + 'enjoy%s.csv'%city, nrows=nrows)
        else:
            print('Invalid provider')

        return df
