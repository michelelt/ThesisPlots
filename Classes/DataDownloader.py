#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ssl
import pymongo
import pandas as pd
from math import *
import json

from .Car2goFormatter import Car2goFormatter



class DataDownloader:
	def __init__(self, init_date=None, final_date=None):
		self.init_date = init_date
		self.final_date = final_date
		self.df = None
		self.city = None
		self.provider=''


	def setup_mongodb(self, CollectionName):
		""""Setup mongodb session """
		try:
			client = pymongo.MongoClient('bigdatadb.polito.it',
										 27017,
										 ssl=True,
										 ssl_cert_reqs=ssl.CERT_NONE) # server.local_bind_port is assigned local port                #client = pymongo.MongoClient()
			client.server_info()
			db = client['carsharing'] #Choose the DB to use
			db.authenticate('ictts', 'Ictts16!')#, mechanism='MONGODB-CR') #authentication         #car2go_debug_info = db['DebugInfo'] #Collection for Car2Go watch
			Collection = db[CollectionName] #Collection for Enjoy watch
		except pymongo.errors.ServerSelectionTimeoutError as err:
			print(err)
		return Collection


	def haversine(self, lon1, lat1, lon2, lat2):
		"""
		Calculate the great circle distance between two points
		on the earth (specified in decimal degrees)
		"""
		# convert decimal degrees to radians
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
		# haversine formula
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a))
		km = 6367 * c

		return int(km*1000)


	def post_process_data(self):
		print("Post processing is started")
		self.df["duration"] = self.df["final_time"] - self.df["init_time"]
		self.df["duration"] = self.df["duration"].astype(int)
		print('Duration computed')


		self.df['distance'] = self.df.apply(lambda x : self.haversine(
			   float(x['start_lon']),float(x['start_lat']),
			   float(x['end_lon']), float(x['end_lat'])), axis=1)
		print('Distance computed')

		self.df['Year'] = pd.DatetimeIndex(self.df['init_date']).year
		self.df['Month'] = pd.DatetimeIndex(self.df['init_date']).month
		self.df['Day'] = pd.DatetimeIndex(self.df['init_date']).day
		self.df['Hour'] = pd.DatetimeIndex(self.df['init_date']).hour

		print('DONE!')
		return self.df


	def download_data(self, city='Torino', provider=''):
		self.city = city
		self.provider=provider

		if provider == 'enjoy': provider+='_'
		collection=provider+"PermanentBookings"
		collection_bookings = self.setup_mongodb(collection)

		print('Qurey is started')
		if self.init_date == None and self.init_date == None:
			bookings = collection_bookings.find({"city": city})

		elif self.init_date == None and self.final_date != None:
			bookings = collection_bookings.find({"city": city,
			                                    "init_date": { "$lt": self.final_date }})

		elif self.init_date != None and self.final_date == None:
			bookings = collection_bookings.find({"city": city,
			                                    "init_date": {"$gt": self.init_date},
											   })
		else:
			bookings = collection_bookings.find({"city": city,
			                                    "init_date": {"$gt": self.init_date,
			                                                  "$lt": self.final_date}
											   })

		self.df = pd.DataFrame(list(bookings))
		print("All data queried")


		# c2g formatter is the same of enjoy
		c2g_formatter = Car2goFormatter(self.df)
		self.df = c2g_formatter.get_df()

		self.df.to_csv(provider+city+'.csv')

		self.post_process_data()

		return self.df


	def dump_df(self, path, file_type):
		if file_type == 'csv': self.df.to_csv(path + self.provider + self.city+'.csv', index=False)
		if file_type == 'pickle': self.df.to_pickle(path + self.provider + self.city+'.pickle')



# # =============================================================================
# # 'test df'
# # =============================================================================
# bookings_df = pd.read_csv('backup_data')
# filtered = bookings_df[  (bookings_df.duration >= 60)
#                         &(bookings_df.duration <= 60*60)
#                         &(bookings_df.distance >= 700)]

# init_timestamp = time.mktime(datetime.datetime(2017, 9, 5, 0, 0, 0).timetuple())
# final_timestamp =  time.mktime(datetime.datetime(2017, 11, 2, 23, 59, 59).timetuple())

# test_df = filtered[  (filtered.init_time >= init_timestamp)
#                     &(filtered.final_time <= final_timestamp)
#                 ]

# test_df[['start_lat', 'start_lon', 'end_lat', 'end_lon']].to_csv('car2go_sep_nov.csv')




# # =============================================================================
# # 'dec-jan'
# # =============================================================================
# bookings_df = pd.read_csv('backup_data')
# filtered = bookings_df[  (bookings_df.duration >= 60)
#                         &(bookings_df.duration <= 60*60)
#                         &(bookings_df.distance >= 700)]

# init_timestamp = time.mktime(datetime.datetime(2017, 12, 1, 0, 0, 0).timetuple())
# final_timestamp =  time.mktime(datetime.datetime(2018, 1, 31, 23, 59, 59).timetuple())

# test_df = filtered[  (filtered.init_time >= init_timestamp)
#                     &(filtered.final_time <= final_timestamp)
#                 ]

# test_df[['start_lat', 'start_lon', 'end_lat', 'end_lon']].to_csv('car2go_dec_jan.csv')


# # =============================================================================
# # 'dec-jan'
# # =============================================================================
# bookings_df = pd.read_csv('backup_data')
# filtered = bookings_df[  (bookings_df.duration >= 60)
#                         &(bookings_df.duration <= 60*60)
#                         &(bookings_df.distance >= 700)]

# init_timestamp = time.mktime(datetime.datetime(2017, 6, 1, 0, 0, 0).timetuple())
# final_timestamp =  time.mktime(datetime.datetime(2017, 7, 31, 23, 59, 59).timetuple())

# test_df = filtered[  (filtered.init_time >= init_timestamp)
#                     &(filtered.final_time <= final_timestamp)
#                 ]

# test_df = test_df[['start_lat', 'start_lon', 'end_lat', 'end_lon']]


# bookings_df.to_pickle('bookings_%s_dirty.pickle'%city.replace(' ', '_').lower())
# # bookings_df.to_csv('bookings_%s_dirty.csv'%city.replace(' ', '_').lower())












