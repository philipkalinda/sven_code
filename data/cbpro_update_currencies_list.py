import sys
sys.path.insert(0, '../../../')
import time
import sqlite3
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from sven.src.data import cbpro_queries
from sven.src.data.cbpro_data_handler import CBProDataHandler
from sven.src.data.cbpro_cryptocurrencies import currencies

price_database = '../../data/raw/cbpro_prices.db'

def get_tables(db_location):
    """
    :param db_location:
    :return:
    """

    conn = sqlite3.connect(db_location)
    tables = pd.read_sql_query(cbpro_queries.check_database_tables(), conn)
    conn.close()

    return tables


def update_currencies_list(n_years=5, target_database=price_database):
    """
    :param n_years:
    :param target_database:
    :return:
    """

    tables = get_tables(target_database)
    tables_list = tables.name.tolist()

    crypto = CBProDataHandler(database_location=target_database)

    for curr in tqdm(currencies.keys(), desc='Currency'):
        currency_pair = currencies[curr]['currency_pair']

        if currencies[curr]['database'] not in tables_list:
            print('Accessing Historical Data for {}'.format(currency_pair))
            crypto.get_all_historical_api_data(currency_pair=currency_pair, n_years=n_years)
            print('Historical Data for {} has completed'.format(currency_pair))
            print(f'Allowing API cooldown for 5 seconds...')
            time.sleep(5)
        else:
            print('There is already data in the database for {}'.format(currency_pair))


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    update_currencies_list(n_years=5, target_database=price_database)
    print(f'Ending Script Now: {datetime.now()}...')
