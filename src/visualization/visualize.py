import os
import sys
sys.path.insert(0, '../../../')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


def visualize(df, default_thresholds, symbol, start_index=0, end_index=None, latest=False):

	df = df.sort_values(by='date').reset_index(drop=True)

	fig = plt.figure(figsize=(16, 16))

	if latest:
		end_index = df.shape[0]
		start_index = end_index - (365 * 2)
		idx_label = 'recent'
	else:
		start_index = start_index
		if end_index is None:
			end_index = df.shape[0]
		idx_label = 'all'
	########################################################
	# SMA
	ax1 = plt.subplot(5, 1, 1)
	df.iloc[start_index:end_index][
		['close'] + \
		sorted([i for i in df.columns if i[:3] == 'SMA'], key=lambda y: int(y.split('_')[1]))
		].plot(ax=ax1, title=f'{symbol} - SMA')
	(df.iloc[start_index:end_index]['from_buy_sma_crossover_indicator'] * 100).plot(ax=ax1, secondary_y=True, color='green', alpha=0.6)
	(df.iloc[start_index:end_index]['from_sell_sma_crossover_indicator'] * 100).plot(ax=ax1, secondary_y=True, color='red', alpha=0.6)

	(df.iloc[start_index:end_index]['to_buy_sma_crossover_indicator'] * 100).plot(ax=ax1, secondary_y=True, color='green', alpha=0.6)
	(df.iloc[start_index:end_index]['to_sell_sma_crossover_indicator'] * 100).plot(ax=ax1, secondary_y=True, color='red', alpha=0.6)

	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].sma_buy_area == 1].index:
		ax1.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.025, color='green')
	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].sma_sell_area == 1].index:
		ax1.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.025, color='red')

	########################################################
	# RSI
	ax2 = plt.subplot(5, 1, 2)
	df.iloc[start_index:end_index][[
		'close'
	]].plot(ax=ax2, title=f'{symbol} - RSI')

	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].rsi_buy_indicator == 1].index:
		ax2.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.2, color='green')
	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].rsi_sell_indicator == 1].index:
		ax2.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.2, color='red')

	########################################################
	# MACD
	ax3 = plt.subplot(5, 1, 3)
	df.iloc[start_index:end_index][[
		'close'
	]].plot(ax=ax3, title=f'{symbol} - MACD')

	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].macd_buy_indicator == 1].index:
		ax3.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.2, color='green')
	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].macd_sell_indicator == 1].index:
		ax3.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.2, color='red')

	########################################################
	# STOCHRSI
	ax4 = plt.subplot(5, 1, 4)
	df.iloc[start_index:end_index][[
		'close'
	]].plot(ax=ax4, title=f'{symbol} - StochRSI')

	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].stoch_rsi_buy_indicator == 1].index:
		ax4.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.2, color='green')
	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].stoch_rsi_sell_indicator == 1].index:
		ax4.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.2, color='red')

	########################################################
	# BBANDS
	ax5 = plt.subplot(5, 1, 5)
	df.iloc[start_index:end_index][[
		'close'
	]].plot(ax=ax5, title=f'{symbol} - BBands')

	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].bb_buy_indicator == 1].index:
		ax5.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.2, color='green')
	for i in df.iloc[start_index:end_index][df.iloc[start_index:end_index].bb_sell_indicator == 1].index:
		ax5.axvspan(xmin=i, xmax=i + 1, ymin=0, ymax=1, alpha=0.2, color='red')

	########################################################
	# Final Signals
	# ax6 = plt.subplot(6, 1, 5)

	# ax6.plot()
	# ax6.plot()

	########################################################
	plt.legend()
	#     plt.savefig(f'{symbol}_{df.date.max()}_{idx_label}.png')
	plt.show()