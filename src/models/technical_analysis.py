import sys
import os
from pathlib import Path
sys.path.insert(0, '../../../')
from sven.src.models import ta_algo_queries
from tqdm import tqdm
import pandas as pd
import sqlite3
from datetime import datetime


class Algorithm():

	def __init__(self, database_location):
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

	# todo: add total number of signals to indicate strength of signals too
	@staticmethod
	def check_signals(data, symbol, dt, signal, n_days):

		short_n_days, long_n_days = n_days

		signal_df = pd.DataFrame()
		signal_df['date'] = [dt]
		signal_df['symbol'] = [symbol]
		signal_indicators = [i for i in data.columns if signal in i]
		for day_lookback in n_days:
			# add features for each day lookback
			for indicator in signal_indicators:
				indicator_value = int(data.sort_values('date', ascending=False).head(day_lookback)[indicator].sum() > 0)
				signal_df[indicator + '_' + str(day_lookback)] = [indicator_value]
				# todo: add logic to only include RSI?
				if 'rsi' in indicator:
					indicator_sum = data.sort_values('date', ascending=False).head(day_lookback)[indicator].sum()
					signal_df['sum_' + indicator + '_' + str(day_lookback)] = [indicator_sum]

			# day_lookback_total = signal_df[[i for i in signal_df.columns if str(day_lookback) in i]].sum(axis=1)
			day_lookback_total = signal_df[[i for i in signal_df.columns if str(day_lookback) in i and 'sum' not in i]].sum(axis=1)
			signal_df['total_' + str(day_lookback)] = day_lookback_total

		# show how salient shorter period is
		signal_df['recency_ratio'] = signal_df['total_' + str(short_n_days)] / signal_df['total_' + str(long_n_days)]

		grand_total = signal_df[[i for i in signal_df.columns if 'total' in i]].sum(axis=1)
		signal_df['total_all'] = grand_total

		return signal_df

	def add_macd_rsi_strategy_flag(self, signal_data, n_days, signal):

		short_n_days, long_n_days = n_days

		signal_data['macd_rsi_strategy_flag'] = signal_data.apply(
			lambda row: 1 if row['macd_' + signal + '_indicator_' + str(short_n_days)] == 1 and \
			                 row['rsi_' + signal + '_indicator_' + str(long_n_days)] == 1 \
						else 0, axis=1
		)

		return signal_data

	def update_all_signals(self, strategy, n_days=(5,14), signal='buy'):

		strategy_db_location = f'../../data/processed/ta_processed_{strategy}.db'
		strategy_conn = sqlite3.connect(strategy_db_location)

		input_tables = pd.read_sql_query(ta_algo_queries.check_database_tables(), strategy_conn)
		symbol_list = input_tables.name.tolist()

		today_dt = str(datetime.today().date())
		dt_table_name = f'{signal}_' + today_dt.replace('-', '_')

		final_df = pd.DataFrame()
		for n, symbol in tqdm(enumerate(symbol_list), desc='Symbol'):
			print(f'[{signal}/{strategy}] Updating Technical Analysis Signal Check for [{n + 1}/{len(symbol_list)}] {symbol}...')

			df = pd.read_sql_query(ta_algo_queries.get_all_data(table=symbol), strategy_conn)
			dt = df.date.max()

			signal_df = self.check_signals(data=df, symbol=symbol, dt=dt, n_days=n_days, signal=signal)

			output_df = self.add_macd_rsi_strategy_flag(signal_data=signal_df, n_days=n_days, signal=signal)

			final_df = final_df.append(output_df)

		if signal == 'buy':
			sorting_order_columns = [
				f'macd_{signal}_indicator_',
				f'sum_rsi_{signal}_indicator_',
				f'sum_stoch_rsi_{signal}_indicator_',
				f'rsi_{signal}_indicator_',
				f'sma_{signal}_area_',
				f'from_{signal}_sma_crossover_indicator_',
				f'stoch_rsi_{signal}_indicator_',
				f'bb_{signal}_indicator_'
			]

			final_df = final_df.sort_values(
				by=[f'macd_rsi_strategy_flag'] + \
					[f'macd_{signal}_indicator_{str(n_days[0])}'] + \
					[f'sum_rsi_{signal}_indicator_{str(n_days[1])}', f'sum_rsi_{signal}_indicator_{str(n_days[0])}'] + \
					[f'sum_stoch_rsi_{signal}_indicator_{str(n_days[1])}', f'sum_stoch_rsi_{signal}_indicator_{str(n_days[0])}'] + \
					[f'total_{n_days[0]}', f'total_{n_days[1]}'] + \
					[i + str(n_days[0]) for i in sorting_order_columns] + \
					[i + str(n_days[1]) for i in sorting_order_columns],
				ascending=False
			)

		if signal == 'sell':
			sorting_order_columns = [
				f'macd_{signal}_indicator_',
				f'sum_rsi_{signal}_indicator_',
				f'sum_stoch_rsi_{signal}_indicator_',
				f'rsi_{signal}_indicator_',
				f'sma_{signal}_area_',
				f'from_{signal}_sma_crossover_indicator_',
				f'stoch_rsi_{signal}_indicator_',
				f'bb_{signal}_indicator_'
			]

			final_df = final_df.sort_values(
				by=[f'macd_rsi_strategy_flag'] + \
					[f'sum_rsi_{signal}_indicator_{str(n_days[1])}', f'sum_rsi_{signal}_indicator_{str(n_days[0])}'] + \
					[f'sum_stoch_rsi_{signal}_indicator_{str(n_days[1])}', f'sum_stoch_rsi_{signal}_indicator_{str(n_days[0])}'] + \
					[f'total_{n_days[0]}', f'total_{n_days[1]}'] + \
					[i + str(n_days[0]) for i in sorting_order_columns] + \
					[i + str(n_days[1]) for i in sorting_order_columns],
				ascending=False
			)

		final_df['run_date'] = today_dt

		strategy_conn.close()

		self.access_database()
		final_df.to_sql(dt_table_name, con=self.conn, if_exists='replace', index=False)
		self.conn.commit()
		self.close_database_connection()


