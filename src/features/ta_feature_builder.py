import os
import sys
sys.path.insert(0, '../../../')
import pandas as pd
import numpy as np
import sqlite3
import pandas_ta as ta
from pathlib import Path
from datetime import datetime
from sven.src.features import ta_queries


class TAFeatureBuilder:

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


	@staticmethod
	def process_data(df, n_years=5):
		"""
		:param df:
		:return:
		"""

		df = df.sort_values(by='date').reset_index(drop=True)
		df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
		df['date'] = df.date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
		df = df[df.date.apply(lambda x: ((datetime.today().date() - x).days / 365) < n_years)]
		df = df.sort_values(by='date', ascending=True).reset_index(drop=True)

		return df

	@staticmethod
	def rsi_buy_indicator(df, params):
		col = [i for i in df.columns if i[:3] == 'RSI'][0]
		buy_indicator = []
		for n, row in df.iterrows():
			if n >= 1:
				if row[col] < params['rsi_lower_threshold']:
					buy_indicator.append(1)  # buy
				else:
					buy_indicator.append(0)
			else:
				buy_indicator.append(0)
		return buy_indicator

	@staticmethod
	def rsi_sell_indicator(df, params):
		col = [i for i in df.columns if i[:3] == 'RSI'][0]
		buy_indicator = []
		for n, row in df.iterrows():
			if n >= 1:
				if row[col] > params['rsi_upper_threshold']:
					buy_indicator.append(1)  # sell
				else:
					buy_indicator.append(0)
			else:
				buy_indicator.append(0)
		return buy_indicator

	@staticmethod
	def running_macd_std(df, params):
		"""
		:param df:
		:param params:
		:return:
		"""
		col = [i for i in df.columns if i[:5] == 'MACDs'][0]
		upper = []
		lower = []
		for idx, row in df.iterrows():
			try:
				new_mean = df.iloc[idx - params['macd_days_to_calc_std']:idx][col].mean()
				new_std = df.iloc[idx - params['macd_days_to_calc_std']:idx][col].std()

				u = new_mean + (new_std * params['macd_std'])
				l = new_mean - (new_std * params['macd_std'])

				upper.append(u)
				lower.append(l)
			except:
				upper.append(np.nan)
				lower.append(np.nan)

		return upper, lower

	@staticmethod
	def macd_buy_inidcator(df):
		"""

		:param df:
		:return:
		"""
		hist_col = [i for i in df.columns if i[:5] == 'MACDh'][0]
		signal_col = [i for i in df.columns if i[:5] == 'MACDs'][0]
		buy_indicator = []
		for n, row in df.iterrows():
			if n >= 1:
				if np.sign(row[hist_col]) == 1 \
						and np.sign(df.iloc[n - 1][hist_col]) == -1 \
						and row[signal_col] <= row['macd_lower_bound']:
					buy_indicator.append(1)  # buy
				else:
					buy_indicator.append(0)
			else:
				buy_indicator.append(0)
		return buy_indicator

	@staticmethod
	def macd_sell_inidcator(df):
		"""

		:param df:
		:return:
		"""
		hist_col = [i for i in df.columns if i[:5] == 'MACDh'][0]
		signal_col = [i for i in df.columns if i[:5] == 'MACDs'][0]
		sell_indicator = []
		for n, row in df.iterrows():
			if n >= 1:
				if np.sign(row[hist_col]) == -1 \
						and np.sign(df.iloc[n - 1][hist_col]) == 1 \
						and row[signal_col] >= row['macd_upper_bound']:
					sell_indicator.append(1)  # sell
				else:
					sell_indicator.append(0)
			else:
				sell_indicator.append(0)
		return sell_indicator

	@staticmethod
	def stoch_rsi_buy_indicator(df, params):
		col = [i for i in df.columns if i[:9] == 'STOCHRSId'][0]
		buy_indicator = []
		for n, row in df.iterrows():
			if n >= 1:
				if row[col] < params['stoch_rsi_lower_threshold']:
					buy_indicator.append(1)  # buy
				else:
					buy_indicator.append(0)
			else:
				buy_indicator.append(0)
		return buy_indicator

	@staticmethod
	def stoch_rsi_sell_indicator(df, params):
		col = [i for i in df.columns if i[:9] == 'STOCHRSId'][0]
		buy_indicator = []
		for n, row in df.iterrows():
			if n >= 1:
				if row[col] > params['stoch_rsi_upper_threshold']:
					buy_indicator.append(1)  # sell
				else:
					buy_indicator.append(0)
			else:
				buy_indicator.append(0)
		return buy_indicator

	@staticmethod
	def running_bb_std(df, params):
		"""

		:param df:
		:param params:
		:return:
		"""
		upper_col = [i for i in df.columns if i[:3] == 'BBU'][0]
		lower_col = [i for i in df.columns if i[:3] == 'BBL'][0]
		lower = []
		upper = []
		for idx, row in df.iterrows():
			try:
				l_new_mean = (df.iloc[idx - params['bbands_days_to_calc_std']:idx]['close'] \
							- df.iloc[idx - params['bbands_days_to_calc_std']:idx][lower_col]).mean()
				u_new_mean = (df.iloc[idx - params['bbands_days_to_calc_std']:idx][upper_col] \
							- df.iloc[idx - params['bbands_days_to_calc_std']:idx]['close']).mean()

				l_new_std = (df.iloc[idx - params['bbands_days_to_calc_std']:idx]['close'] \
							- df.iloc[idx - params['bbands_days_to_calc_std']:idx][lower_col]).std()
				u_new_std = (df.iloc[idx - params['bbands_days_to_calc_std']:idx][upper_col] \
							- df.iloc[idx - params['bbands_days_to_calc_std']:idx]['close']).std()

				l_val = l_new_mean + (l_new_std * params['bbands_diff_std'])
				u_val = u_new_mean + (u_new_std * params['bbands_diff_std'])

				lower.append(l_val)
				upper.append(u_val)
			except:
				lower.append(np.nan)
				upper.append(np.nan)

		return upper, lower

	@staticmethod
	def bb_buy_inidcator(df):
		"""

		:param df:
		:return:
		"""
		upper_col = [i for i in df.columns if i[:3] == 'BBU'][0]
		buy_indicator = []
		for n, row in df.iterrows():
			signal = row[upper_col] - row['close']
			if signal > row['bb_upper_bound']:
				buy_indicator.append(1)
			else:
				buy_indicator.append(0)
		return buy_indicator

	@staticmethod
	def bb_sell_inidcator(df):
		"""

		:param df:
		:return:
		"""
		lower_col = [i for i in df.columns if i[:3] == 'BBL'][0]
		sell_indicator = []
		for n, row in df.iterrows():
			signal = row['close'] - row[lower_col]
			if signal > row['bb_lower_bound']:
				sell_indicator.append(1)
			else:
				sell_indicator.append(0)
		return sell_indicator

	# todo: re-work crossovers in order to get crossover_to_buy_area and crossover_to_sell_area
	@staticmethod
	def sma_crossover_predict(df, params):
		"""

		:param df:
		:param params:
		:return:
		"""
		smas = sorted([i for i in df.columns if i[:3] == 'SMA'], key=lambda y: int(y.split('_')[1]))
		fast_sma = smas[0]
		slow_sma = smas[-1]
		from_sell_position_crossover = []
		from_buy_position_crossover = []

		for n, row in df.iterrows():

			if n < params['sma_lookback'] \
					or np.isnan(row[fast_sma]) \
					or np.isnan(row[slow_sma]) \
					or np.isnan(df.iloc[n - params['sma_lookback']][fast_sma]) \
					or np.isnan(df.iloc[n - params['sma_lookback']][slow_sma]):
				from_sell_position_crossover.append(0)
				from_buy_position_crossover.append(0)
			else:
				x_fast = range(params['sma_lookback'])
				y_fast = df.iloc[n - params['sma_lookback']:n][fast_sma].tolist()
				x_slow = range(params['sma_lookback'])
				y_slow = df.iloc[n - params['sma_lookback']:n][slow_sma].tolist()

				x_pred = range(params['sma_lookback'], params['sma_lookback'] + params['sma_crossover_forecast'])

				coef_fast = np.polyfit(x_fast, y_fast, 1)
				coef_slow = np.polyfit(x_slow, y_slow, 1)

				poly1d_fn_fast = np.poly1d(coef_fast)
				poly1d_fn_slow = np.poly1d(coef_slow)

				signal = []
				ordering = {'above': None, 'below': None}

				if poly1d_fn_fast(x_pred[0]) > poly1d_fn_slow(x_pred[0]):
					ordering['above'] = poly1d_fn_fast(x_pred)
					ordering['below'] = poly1d_fn_slow(x_pred)
					position = 'from_sell'
				else:
					ordering['above'] = poly1d_fn_slow(x_pred)
					ordering['below'] = poly1d_fn_fast(x_pred)
					position = 'from_buy'

				for n, (i, j) in enumerate(zip(ordering['above'], ordering['below'])):
					if i > j:
						signal.append(0)
					elif i <= j:
						signal.append(1)
					else:
						signal.append(0)

				if sum(signal) > 0:
					if position == 'from_sell':
						from_sell_position_crossover.append(1)
						from_buy_position_crossover.append(0)
					if position == 'from_buy':
						from_buy_position_crossover.append(1)
						from_sell_position_crossover.append(0)
				else:
					from_buy_position_crossover.append(0)
					from_sell_position_crossover.append(0)
		return from_buy_position_crossover, from_sell_position_crossover

	@staticmethod
	def sma_buy_area(df):
		"""

		:param df:
		:param params:
		:return:
		"""
		smas = sorted([i for i in df.columns if i[:3] == 'SMA'], key=lambda y: int(y.split('_')[1]))
		fast_sma = smas[0]
		slow_sma = smas[-1]

		buy_area = (df[fast_sma] < df[slow_sma]).apply(int).tolist()

		return buy_area

	@staticmethod
	def sma_sell_area(df):
		"""

		:param df:
		:param params:
		:return:
		"""
		smas = sorted([i for i in df.columns if i[:3] == 'SMA'], key=lambda y: int(y.split('_')[1]))
		fast_sma = smas[0]
		slow_sma = smas[-1]

		buy_area = (df[fast_sma] > df[slow_sma]).apply(int).tolist()

		return buy_area

	def generate_features(self, input_df, params, strategy):
		"""

		:param input_df:
		:param params:
		:param strategy:
		:return:
		"""

		print('Generating Features...')
		output_df = self.process_data(input_df, n_years=10)

		# apply technical analysis strategy
		output_df.ta.strategy(strategy)

		# SMA Features
		output_df['sma_buy_area'] = self.sma_buy_area(df=output_df)
		output_df['sma_sell_area'] = self.sma_sell_area(df=output_df)

		from_buy_indicator, from_sell_indicator = self.sma_crossover_predict(df=output_df, params=params)
		output_df['from_buy_sma_crossover_indicator'] = from_buy_indicator
		output_df['from_sell_sma_crossover_indicator'] = from_sell_indicator
		output_df['to_buy_sma_crossover_indicator'] = from_sell_indicator
		output_df['to_sell_sma_crossover_indicator'] = from_buy_indicator

		# RSI Features
		output_df['rsi_buy_indicator'] = self.rsi_buy_indicator(df=output_df, params=params)
		output_df['rsi_sell_indicator'] = self.rsi_sell_indicator(df=output_df, params=params)
		# todo: add features to show coming out of RSI period as a proxy for the sell

		# MACD Features
		macd_upper, macd_lower = self.running_macd_std(df=output_df, params=params)
		output_df['macd_upper_bound'] = macd_upper
		output_df['macd_lower_bound'] = macd_lower
		output_df['macd_buy_indicator'] = self.macd_buy_inidcator(df=output_df)
		output_df['macd_sell_indicator'] = self.macd_sell_inidcator(df=output_df)

		# StochRSI Features
		output_df['stoch_rsi_buy_indicator'] = self.stoch_rsi_buy_indicator(df=output_df, params=params)
		output_df['stoch_rsi_sell_indicator'] = self.stoch_rsi_sell_indicator(df=output_df, params=params)

		# BB Features
		bb_upper, bb_lower = self.running_bb_std(df=output_df, params=params)
		output_df['bb_upper_bound'] = bb_upper
		output_df['bb_lower_bound'] = bb_lower
		output_df['bb_buy_indicator'] = self.bb_buy_inidcator(df=output_df)
		output_df['bb_sell_indicator'] = self.bb_sell_inidcator(df=output_df)

		return output_df

	def update_ta_database(self, input_df, symbol, params, strategy):
		"""

		:param input_df:
		:param symbol:
		:param params:
		:param strategy:
		:return:
		"""
		if input_df.shape[0] >= 200:

			# initiate database connection
			self.access_database()

			tables = pd.read_sql_query(ta_queries.check_database_tables(), self.conn)

			if symbol in tables.name.tolist():
				# drop table if it exists
				self.cursor.execute(ta_queries.drop_table(symbol))
				self.conn.commit()

			features_df = self.generate_features(input_df, params, strategy)

			features_df.to_sql(symbol, self.conn, if_exists='replace', index=False)
			self.conn.commit()

			# close connection
			self.close_database_connection()

		else:
			print('There is not enough data to generate all features...')


	def get_all_data(self, symbol):
		"""
		:param symbol:
		:return:
		"""

		self.access_database()

		print(f'Retrieving Data for {symbol}...')
		data = pd.read_sql_query(ta.get_all_data(table=symbol), self.conn)

		self.close_database_connection()

		return data

