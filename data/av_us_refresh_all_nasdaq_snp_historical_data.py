import sys
import time
import sqlite3
import pandas as pd
from datetime import datetime
sys.path.insert(0, '../../../')
from sven.src.data import av_us_queries
from sven.src.data.av_us_data_handler import AVUSDataHandler


price_database = '../../data/raw/av_us_prices.db'
listing_database = '../../data/external/us_listings.db'


def get_symbols(listing_db=listing_database):
    """
    :param listing_db:
    :return:
    """

    conn = sqlite3.connect(listing_db)

    df = pd.read_sql_query(av_us_queries.get_all_data('nasdaq_100_list'), conn)
    df2 = pd.read_sql_query(av_us_queries.get_all_data('sandp_100_list'), conn)
    symbol_list = list(set(df.symbol.tolist() + df2.symbol.tolist()))

    conn.close()

    return symbol_list


def refresh_all_historical_data(price_db=price_database, listing_db=listing_database):
    """
    :param price_db:
    :param listing_db:
    :return:
    """

    symbols_list = get_symbols(listing_db=listing_db)
    data_handler = AVUSDataHandler(database_location=price_db)

    s = time.time()
    for n, symbol in enumerate(symbols_list):

        indicator = (n + 1) % 5
        if indicator == 0:
            e = time.time()
            compute_time = e - s
            print('The Compute time is: {}'.format(compute_time ))
            print('The rest time is 65 - {} = {}'.format(compute_time, 65-compute_time))
            print('Resting API calls...')
            time.sleep(60)
            s = time.time()
        try:
            print('Accessing Historical Data for {} [{}/{}]'.format(symbol, n + 1, len(symbols_list)))
            data_handler.refresh_all_historical_data(symbol=symbol)
        except:
            continue


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    refresh_all_historical_data(price_db=price_database, listing_db=listing_database)
    print(f'Ending Script Now: {datetime.now()}...')