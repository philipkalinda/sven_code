import os
import sys
from pathlib import Path
sys.path.insert(0, '../../../')

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import cbpro

from sven.src.data import cbpro_queries
from sven.src.data.cbpro_cryptocurrencies import currencies


class CBProDataHandler:
	"""
	This class is dedicated to Handling data from crypto sources
	"""

	def __init__(self, database_location='../../data/raw/cbpro_prices.db'):
		"""
		:param database_location:
		"""

		self.client = cbpro.PublicClient()
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

	def query_data(self, currency_pair, date_list):
		"""
		:param currency_pair:
		:param date_list:
		:return:
		"""

		queried_data_list = []
		# loop through dates between

		if len(date_list) <= 300:
			start_date = date_list[0]
			end_date = date_list[-1]
			print(f'Querying Data for {currency_pair} [start: {start_date}, end: {end_date}]...')
			queried_data = self.client.get_product_historic_rates(
				currency_pair,
				start=start_date,
				end=end_date,
				granularity=86400
			)
			if len(queried_data) > 0:
				queried_data_list += queried_data

		else:
			dt_list = date_list.copy()
			broken_down_dates_list = []
			while len(dt_list) > 0:
				broken_down_dates_list.append(dt_list[:300])
				del dt_list[:300]

			# loop through broken down list due to API rate limiting from cbpro
			for bd_dt_list in broken_down_dates_list:
				start_date = bd_dt_list[0]
				end_date = bd_dt_list[-1]
				print(f'Querying Data for {currency_pair} [start: {start_date}, end: {end_date}]...')
				queried_data = self.client.get_product_historic_rates(
					currency_pair,
					start=start_date,
					end=end_date,
					granularity=86400
				)

				if len(queried_data) > 0:
					queried_data_list += queried_data

		final_query_data = []
		for row in queried_data_list:
			row[0] = datetime.fromtimestamp(row[0]).date().__str__()
			final_query_data.append(row)


		print(f'Finished Querying Data for {currency_pair}...')

		return final_query_data

	@staticmethod
	def process_queried_data(queried_data_list):
		"""
		:param queried_data_list:
		:return:
		"""
		print('Processing Data...')
		# process suitable for database entry
		data_to_store = ', '.join([str(tuple(i)) for i in queried_data_list])

		return data_to_store

	def get_all_historical_api_data(self, currency_pair='BTC-USD', n_years=5):
		"""
		get all the historical data
		:param currency_pair:
		:param n_years:
		:return:
		"""

		print(f'Getting historical data for {currency_pair}...')
		# access database
		self.access_database()

		base = (datetime.today() - timedelta(days=1)).date()
		date_list = sorted([base - timedelta(days=x) for x in range(n_years * 365)])

		queried_data_list = self.query_data(currency_pair=currency_pair, date_list=date_list)
		# loop through dates between

		if len(queried_data_list) > 0:
			# process data
			data_to_store = self.process_queried_data(queried_data_list=queried_data_list)

			tables = pd.read_sql_query(cbpro_queries.check_database_tables(), self.conn)

			# drop current table if in database
			if currencies[currency_pair]['database'] in tables.name.tolist():
				self.cursor.execute(cbpro_queries.drop_table(table=currencies[currency_pair]['database']))
				self.conn.commit()

			# re-create the table
			self.cursor.execute(cbpro_queries.create_table(table=currencies[currency_pair]['database']))
			self.conn.commit()

			# enter the data into the database
			self.cursor.execute(cbpro_queries.insert_data(table=currencies[currency_pair]['database'], values=data_to_store))
			self.conn.commit()

			# close database connection
			self.close_database_connection()

		else:
			print('INFO: There is no Data available for {currency_pair}')

		print(f'Finished getting historical data for {currency_pair}...')

	def update_database(self, currency_pair='BTC-USD'):
		"""
		update the database for the particular currency pair
		:param currency_pair:
		:return:
		"""

		# access database
		self.access_database()

		currency_table = currencies[currency_pair]['database']

		self.cursor.execute(cbpro_queries.get_max_date(table=currency_table))
		start_date_queried = self.cursor.fetchall()[0][0]

		start_date = datetime.strptime(start_date_queried, '%Y-%m-%d').date()

		end_date = (datetime.today() - timedelta(days=1)).date()

		days_between = (end_date - start_date).days

		if days_between == 0:
			print(f"Data for {currency_pair} is already up to date...")
			return True
		else:
			print(f"Data is being updated for {currency_pair} for {days_between} days...")

		# list of dates between dates
		date_list = sorted([end_date - timedelta(days=x) for x in range(days_between)])

		queried_data_list = self.query_data(currency_pair=currency_pair, date_list=date_list)

		# process data
		data_to_store = self.process_queried_data(queried_data_list=queried_data_list)

		# enter the data into the database
		print('Inserting Data into Database...')
		self.cursor.execute(cbpro_queries.insert_data(table=currencies[currency_pair]['database'], values=data_to_store))
		self.conn.commit()

		# close database connection
		self.close_database_connection()

	def get_all_data(self, currency_pair='BTC-USD'):
		"""
		:param currency_pair:
		:return:
		"""

		self.access_database()

		print(f'Retrieving Data for {currency_pair}...')
		data = pd.read_sql_query(cbpro_queries.get_all_data(table=currencies[currency_pair]['database']), self.conn)

		self.close_database_connection()

		return data


if __name__ == '__main__':

	crypto = CBProDataHandler()
	print('Successfully Created CBProDataHandler...')
