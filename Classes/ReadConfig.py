import json
import datetime

class ReadConfig:

    # def __init__(self, config_path):
    #     with open(config_path) as fp: config = json.load(fp)
    #     if 'init_date' in config.keys():
    #         config['init_date'] = datetime.datetime.strptime(config['init_date'], '%Y-%m-%dT%H:%M:%S')
    #         config['init_time'] = datetime.datetime.timestamp(config['init_date'])
    #
    #     if 'final_date' in config.keys():
    #         config['final_date'] = datetime.datetime.strptime(config['final_date'], '%Y-%m-%dT%H:%M:%S')
    #         config['final_time'] = datetime.datetime.timestamp(config['final_date'])
    #
    #     self.config = config

    def __new__(cls, config_path):
        with open(config_path) as fp: config = json.load(fp)
        if 'init_date' in config.keys():
            config['init_date'] = datetime.datetime.strptime(config['init_date'], '%Y-%m-%dT%H:%M:%S')
            config['init_time'] = datetime.datetime.timestamp(config['init_date'])

        if 'final_date' in config.keys():
            config['final_date'] = datetime.datetime.strptime(config['final_date'], '%Y-%m-%dT%H:%M:%S')
            config['final_time'] = datetime.datetime.timestamp(config['final_date'])

        return config


    def get_config(self): return self.config
