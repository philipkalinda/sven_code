import sys
sys.path.insert(0, '../../../')
import time
from tqdm import tqdm
from datetime import datetime
from sven.src.data.cbpro_data_handler import CBProDataHandler
from sven.src.data.cbpro_cryptocurrencies import currencies

price_database = '../../data/raw/cbpro_prices.db'

def update_all_database_tables(n_years=5, target_database=price_database, api_cooldown_s=5):
    """
    This is to loop through and update all the tables in the database with the lastest prices and dates
    :return:
    """
    crypto = CBProDataHandler(database_location=target_database)

    for n, curr in tqdm(enumerate(currencies.keys()), desc='Currency'):
        currency_pair = currencies[curr]['currency_pair']
        print(f'Updating Data for {currency_pair} [{n+1}/{len(currencies.keys())}]...')
        try:
            crypto.update_database(currency_pair=currency_pair)
        except:
            print(curr, ' is not in DB, extracting data for this asset...')
            crypto.get_all_historical_api_data(currency_pair=currency_pair, n_years=n_years)
        print(f'Data has been updated for {currency_pair}...')
        print(f'Allowing API cooldown for {api_cooldown_s} seconds...')
        time.sleep(api_cooldown_s)


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    update_all_database_tables(target_database=price_database)
    print(f'Ending Script Now: {datetime.now()}...')
