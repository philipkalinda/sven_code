import sys
from tqdm import tqdm
import pandas as pd
from datetime import datetime
sys.path.insert(0, '../../../')
from sven.src.data.cbpro_cryptocurrencies import currencies
from sven.src.data.cbpro_data_handler import CBProDataHandler
from sven.src.features.ta_config import config
from sven.src.features.ta_strategies import strategies
from sven.src.features.ta_feature_builder import TAFeatureBuilder


raw_data_database = '../../data/raw/cbpro_prices.db'
ta_database = '../../data/processed/ta_processed_{}.db'


def update_all_database_tables(raw_data_db=raw_data_database, ta_db=ta_database):
    """
    This is to loop through and update all the tables in the database with the lastest prices and dates
    :return:
    """
    for risk_type in config.keys():
        print(f'Building Data for Profile: {risk_type}...')
        data_handler = CBProDataHandler(database_location=raw_data_db)
        feature_generator = TAFeatureBuilder(database_location=ta_db.format(risk_type))

        config_requirement = max(config[risk_type].values())

        for n, curr in tqdm(enumerate(currencies.keys()), desc='Currency'):
            currency_pair = currencies[curr]['currency_pair']
            currency_name = currencies[curr]['currency_name']
            try:
                print(f'Updating Technical Analysis Data for {currency_pair} [{n+1}/{len(currencies.keys())}]...')
                # Get all the raw price data
                raw_data = data_handler.get_all_data(currency_pair=currency_pair)

                if raw_data.shape[0] >= config_requirement:
                    # generate features and update to database
                    feature_generator.update_ta_database(
                        input_df=raw_data,
                        symbol=currencies[curr]['database'],
                        params=config[risk_type],
                        strategy=strategies[risk_type]
                    )
                else:
                    print('Not Enough Data. Skipping Feature building...')
            except:
                print(f'ERROR: Issues creating features for {currency_name} [{currency_pair}]')


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    update_all_database_tables(raw_data_db=raw_data_database, ta_db=ta_database)
    print(f'Ending Script Now: {datetime.now()}...')
