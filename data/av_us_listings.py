import sys
sys.path.insert(0, '../../../')
import os
import requests
import sqlite3
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from sven.src.data import av_us_queries


database_location = '../../data/external/us_listings.db'
# table_name = 'sandp_100_list'
# table_name = 'nasdaq_100_list'


def clean_for_search_term(input_name):
    output_name = input_name.split(',')[0].lower().replace('inc.', '').replace('corporation', '').lower()
    return output_name


def generate_new_nasdaq_100_companies(db_location=database_location, table_name='nasdaq_100_list'):

	print('Acessing Online data for nasdaq 100 list...')
	# website_url = requests.get('https://en.wikipedia.org/wiki/S%26P_100').text
	website_url = requests.get('https://en.wikipedia.org/wiki/NASDAQ-100').text
	soup = BeautifulSoup(website_url, 'lxml')

	table = soup.find('table', {'class': 'wikitable sortable', 'id': 'constituents'})
	results = table.findAll('tr')

	print('Processing Online Data...')
	data = []
	for record in results[1:]:
		row = record.text.split('\n')[1:-1]

		# this is for sandp_100
		# row = [row[i] for i in (0, 2, 4)]

		data.append(row)

	# this is for sandp_100
	# df = pd.DataFrame(columns=['symbol', 'name', 'sector'], data=data)
	# df['searchable_term'] = df.name.apply(lambda n: clean_for_search_term(n))

	# this is for nasdaq_100
	df = pd.DataFrame(columns=['company', 'symbol', 'sector', 'sub_industry'], data=data)
	df['searchable_term'] = df.company.apply(lambda c: clean_for_search_term(c))


	df['etl_inserted'] = datetime.today().date()
	print(df)

	print('Accessing database...')
	if os.path.isfile(db_location):
		conn = sqlite3.connect(db_location)
		print('Connection successful...')
	else:
		print(f'File does not exist: {db_location}...')
		Path(db_location).touch()
		print('Database {} created...'.format(db_location))
		conn = sqlite3.connect(db_location)
		print('Connection successful...')

	df.to_sql(table_name, con=conn, if_exists='replace')
	print('Data Successfully stored within database...')
	conn.close()


def generate_new_sandp_100_companies(db_location=database_location, table_name='sandp_100_list'):

	print('Acessing Online data for nasdaq 100 list...')
	website_url = requests.get('https://en.wikipedia.org/wiki/S%26P_100').text
	# website_url = requests.get('https://en.wikipedia.org/wiki/NASDAQ-100').text
	soup = BeautifulSoup(website_url, 'lxml')

	table = soup.find('table', {'class': 'wikitable sortable', 'id': 'constituents'})
	results = table.findAll('tr')

	print('Processing Online Data...')
	data = []
	for record in results[1:]:
		row = record.text.split('\n')[1:-1]

		# this is for sandp_100
		row = [row[i] for i in (0, 2, 4)]

		data.append(row)

	# this is for sandp_100
	df = pd.DataFrame(columns=['symbol', 'name', 'sector'], data=data)
	df['searchable_term'] = df.name.apply(lambda n: clean_for_search_term(n))

	# this is for nasdaq_100
	# df = pd.DataFrame(columns=['company', 'symbol', 'sector', 'sub_industry'], data=data)
	# df['searchable_term'] = df.company.apply(lambda c: clean_for_search_term(c))


	df['etl_inserted'] = datetime.today().date()
	print(df)

	print('Accessing database...')
	if os.path.isfile(db_location):
		conn = sqlite3.connect(db_location)
		print('Connection successful...')
	else:
		print(f'File does not exist: {db_location}...')
		Path(db_location).touch()
		print('Database {} created...'.format(db_location))
		conn = sqlite3.connect(db_location)
		print('Connection successful...')

	df.to_sql(table_name, con=conn, if_exists='replace')
	print('Data Successfully stored within database...')
	conn.close()


def get_nasdaq_100_companies(db_location=database_location):

	print('Accessing database...')
	if os.path.isfile(db_location):
		conn = sqlite3.connect(db_location)
		print('Connection successful...')
	else:
		print(f'File does not exist: {db_location}...')
		print('Please run `generate_new_nasdaq_100_companies` to create and populate database')
		raise RuntimeError(f'The database could not be connected to [{db_location}]')

	df = pd.read_sql_query(av_us_queries.get_all_data('nasdaq_100_list'), conn)

	conn.close()

	return df


def get_sanp_100_companies(db_location=database_location):

	print('Accessing database...')
	if os.path.isfile(db_location):
		conn = sqlite3.connect(db_location)
		print('Connection successful...')
	else:
		print(f'File does not exist: {db_location}...')
		print('Please run `generate_new_sandp_100_companies` to create and populate database')
		raise RuntimeError(f'The database could not be connected to [{db_location}]')

	df = pd.read_sql_query(av_us_queries.get_all_data('sandp_100_list'), conn)

	conn.close()

	return df


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    generate_new_nasdaq_100_companies(db_location=database_location)
    generate_new_nasdaq_100_companies(db_location=database_location)
    print(f'Ending Script Now: {datetime.now()}...')
