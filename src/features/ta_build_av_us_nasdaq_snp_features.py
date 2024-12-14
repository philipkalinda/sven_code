import sys
import sqlite3
import pandas as pd
from tqdm import tqdm
from datetime import datetime
sys.path.insert(0, '../../../')
from sven.src.data import av_us_queries
from sven.src.data.av_us_data_handler import AVUSDataHandler
from sven.src.features.ta_config import config
from sven.src.features.ta_strategies import strategies
from sven.src.features.ta_feature_builder import TAFeatureBuilder


price_database = '../../data/raw/av_us_prices.db'
listing_database = '../../data/external/us_listings.db'
ta_database = '../../data/processed/ta_processed_{}.db'


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


def update_all_database_tables(price_db=price_database, listing_db=listing_database, ta_db=ta_database):
    """
    :param price_db:
    :param listing_db:
    :param ta_db:
    :return:
    """
    for risk_type in config.keys():
        print(f'Building Data for Profile: {risk_type}...')
        symbols_list = get_symbols(listing_db=listing_db)
        data_handler = AVUSDataHandler(database_location=price_db)
        feature_generator = TAFeatureBuilder(database_location=ta_db.format(risk_type))

        config_requirement = max(config[risk_type].values())

        for n, symbol in tqdm(enumerate(symbols_list), desc='Stock'):

            try:
                print(f'Updating Technical Analysis Data for [{n+1}/{len(symbols_list)}] {symbol}...')
                # Get all the raw price data
                raw_data = data_handler.get_all_data(symbol=symbol)

                if raw_data.shape[0] >= config_requirement:
                    # generate features and update to database
                    feature_generator.update_ta_database(
                        input_df=raw_data,
                        symbol=symbol,
                        params=config[risk_type],
                        strategy=strategies[risk_type]
                    )
                else:
                    print('Not Enough Data. Skipping Feature building...')
            except:
                print('Error Dealing with {}'.format(symbol))


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    update_all_database_tables(price_db=price_database, listing_db=listing_database, ta_db=ta_database)
    print(f'Ending Script Now: {datetime.now()}...')
