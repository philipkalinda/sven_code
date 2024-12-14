import os
import sys
import requests
import numpy as np
from pathlib import Path
sys.path.insert(0, '../../../')

import sqlite3
import pandas as pd
from datetime import datetime, timedelta

from sven.src.data import av_us_queries
from sven.src.credentials import alpha_vantage_credentials


class AVUSDataHandler:
	"""
	This class is dedicated to Handling data from AV for NASDAQ
	"""

	def __init__(self, database_location='../../data/raw/av_us_prices.db'):
		"""
		:param database_location:
		"""

		self.database_location = database_location
		self.conn = None
		self.cursor = None

	def access_database(self):
		"""
		This is to open the connection to the database
		:return:
		"""

		print('Accessing database...')
		if os.path.isfile(self.database_location):
			self.conn = sqlite3.connect(self.database_location)
			print('Connection successful...')
		else:
			print('File does not exist: {}...'.format(self.database_location))
			create = input(f'Would you like to create this database? [{self.database_location}] \n> ')
			if create.lower() == 'y':
				Path(self.database_location).touch()
				print('Database {} created...'.format(self.database_location))
				self.conn = sqlite3.connect(self.database_location)
				print('Connection successful...')
			else:
				raise RuntimeError(f'The database could not be connected to [{self.database_location}]')

		self.cursor = self.conn.cursor()

	def close_database_connection(self):
		"""
		This is to close the connection to the database
		:return:
		"""

		self.conn.close()
		print('Succesfully disconnected from the database...')

	@staticmethod
	def query_data(symbol):
		"""
		:param symbol:
		:return:
		"""

		url = alpha_vantage_credentials['api_base_historical'].format(symbol, alpha_vantage_credentials['api_key'])
		response = requests.get(url)
		data = dict(response.json())

		return data

	@staticmethod
	def process_queried_data(raw_data):
		"""
		:param raw_data:
		:return:
		"""
		print('Processing Data...')
		# process suitable for database entry
		data_list = []
		for dt in raw_data['Time Series (Daily)'].keys():
			data_point = [
				dt,
				np.float(raw_data['Time Series (Daily)'][dt]['1. open']),
				np.float(raw_data['Time Series (Daily)'][dt]['2. high']),
				np.float(raw_data['Time Series (Daily)'][dt]['3. low']),
				np.float(raw_data['Time Series (Daily)'][dt]['4. close']),
				np.float(raw_data['Time Series (Daily)'][dt]['5. volume']),
			]
			data_list.append(data_point)

		data_to_store = ', '.join([str(tuple(i)) for i in data_list[::-1]])

		return data_to_store

	def process_queried_data_for_new_data(self, raw_data, symbol):
		"""
		:param raw_data:
		:param symbol:
		:return:
		"""

		assert raw_data['Meta Data']['2. Symbol'] == symbol, \
			f"""The Symbols do not match | raw data; {raw_data['Meta Data']['2. Symbol']}, symbol passed: {symbol}"""

		print('Extracting New Data...')
		# process suitable for database entry
		self.cursor.execute(av_us_queries.get_max_date(symbol))

		max_date = self.cursor.fetchall()[0][0]
		start_date = datetime.strptime(max_date, '%Y-%m-%d').date()

		end_date = (datetime.today() - timedelta(days=1)).date()

		days_between = (end_date - start_date).days

		date_list = sorted([str(end_date - timedelta(days=x)) for x in range(days_between)])

		print(f'Processing Data From {start_date} To {end_date}...')
		# process suitable for database entry
		data_list = []
		for dt in date_list:
			if dt in raw_data['Time Series (Daily)'].keys():
				data_point = [
					dt,
					raw_data['Time Series (Daily)'][dt]['1. open'],
					raw_data['Time Series (Daily)'][dt]['2. high'],
					raw_data['Time Series (Daily)'][dt]['3. low'],
					raw_data['Time Series (Daily)'][dt]['4. close'],
					raw_data['Time Series (Daily)'][dt]['5. volume'],
				]
				data_list.append(data_point)
			else:
				print(f'No Data Available for {dt}...')

		data_to_store = ', '.join([str(tuple(i)) for i in data_list[::-1]])

		return data_to_store

	def refresh_all_historical_data(self, symbol):
		"""
		:param symbol:
		:return:
		"""

		self.access_database()

		tables = pd.read_sql_query(av_us_queries.check_database_tables(), self.conn)

		if symbol in tables.name.tolist():
			# drop table if it exists
			self.cursor.execute(av_us_queries.drop_table(symbol))
			self.conn.commit()

		# create the table
		self.cursor.execute(av_us_queries.create_table(symbol))
		self.conn.commit()

		print(f'Querying Data for {symbol}...')
		raw_data = self.query_data(symbol=symbol)

		data_to_store = self.process_queried_data(raw_data=raw_data)

		self.cursor.execute(av_us_queries.insert_data(table=symbol, values=data_to_store))
		self.conn.commit()

		self.close_database_connection()

	def update_database(self, symbol):
		"""
		:param symbol:
		:return:
		"""

		# access database
		self.access_database()

		print(f'Querying Data for {symbol}...')
		raw_data = self.query_data(symbol=symbol)

		data_to_store = self.process_queried_data_for_new_data(raw_data=raw_data, symbol=symbol)

		if len(data_to_store) != 0:
			self.cursor.execute(av_us_queries.insert_data(table=symbol, values=data_to_store))
			self.conn.commit()
		else:
			print(f'There is no new data for {symbol}')

		self.close_database_connection()

	def get_all_data(self, symbol):
		"""
		:param symbol:
		:return:
		"""

		self.access_database()

		print(f'Retrieving Data for {symbol}...')
		data = pd.read_sql_query(av_us_queries.get_all_data(table=symbol), self.conn)

		self.close_database_connection()

		return data


if __name__ == '__main__':

	data_handler = AVUSDataHandler()
	print('Successfully Created AVUSDataHandler...')
