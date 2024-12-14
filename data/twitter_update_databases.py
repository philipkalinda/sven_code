import sys
import time
import string
import sqlite3
import pandas as pd
from datetime import datetime
sys.path.insert(0, '../../../')
from sven.src.data import av_us_queries
from sven.src.data.cbpro_cryptocurrencies import currencies
from sven.src.data.twitter_data_handler import TwitterDataHandler


# First we get the listing tables for nasdaq and sandp from this database (we've imported the currencies)
listing_database = '../../data/external/us_listings.db'

# Then we query the listed symbols and place their data in the raw tables within twitter database
av_us_twitter_database = '../../data/raw/av_us_tweets.db'
cbpro_twitter_database = '../../data/raw/cbpro_tweets.db'


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


def update_all_database_tables(price_db=price_database, listing_db=listing_database):
    """
    :param price_db:
    :param listing_db:
    :return:
    """

    symbols_list = get_symbols(listing_db=listing_db)
    data_handler = AVUSDataHandler(database_location=price_db)

    for n, symbol in enumerate(symbols_list):

        if len(set(symbol).intersection(set(string.punctuation))) == 0:

            indicator = (n + 1) % 5
            if indicator == 0:
                print('Resting API calls...')
                time.sleep(60)
            try:
                print('Updating Data for {} [{}/{}]'.format(symbol, n + 1, len(symbols_list)))
                data_handler.update_database(symbol=symbol)
            except:
                print('ERROR: ', symbol, ' is not in DB, extracting data for this asset...')
                try:
                    data_handler.refresh_all_historical_data(symbol=symbol)
                except:
                    print(f'ERROR: Unable to extract data for {symbol}...')
        else:
            print(f'ERROR: Punctuation in {symbol} Therefore not considering')


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    update_all_database_tables(price_db=price_database, listing_db=listing_database)
    print(f'Ending Script Now: {datetime.now()}...')
