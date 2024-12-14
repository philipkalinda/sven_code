import sys
sys.path.insert(0, '../../../')
import time
from tqdm import tqdm
from datetime import datetime
from sven.src.data.cbpro_data_handler import CBProDataHandler
from sven.src.data.cbpro_cryptocurrencies import currencies


price_database = '../../data/raw/cbpro_prices.db'


def refresh_all_historical_data(n_years=5, target_database=price_database):
    """"
    Gets all the historical data for all
    :return:
    """

    crypto = CBProDataHandler(database_location=target_database)

    for curr in tqdm(currencies.keys(), desc='Currency'):
        currency_pair = currencies[curr]['currency_pair']
        print('Accessing Historical Data for {}'.format(currency_pair))
        crypto.get_all_historical_api_data(currency_pair=currency_pair, n_years=n_years)
        print("Historical Data for {} has completed".format(currency_pair))
        print(f'Allowing API cooldown for 5 seconds...')
        time.sleep(5)


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    refresh_all_historical_data(n_years=5, target_database=price_database)
    print(f'Ending Script Now: {datetime.now()}...')
