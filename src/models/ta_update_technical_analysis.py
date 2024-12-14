import sys
from datetime import datetime
sys.path.insert(0, '../../../')
from sven.src.features.ta_config import config
from sven.src.models.technical_analysis import Algorithm


results_database = '../../data/results/ta_results_{}.db'


def update_all_signals(results_db=results_database):

    for risk_type in config.keys():
        print(f'Running Technical Analysis Signal Check for Profile: {risk_type}...')

        signal_checker = Algorithm(database_location=results_db.format(risk_type))

        print('Updating Buy Signals...')
        signal_checker.update_all_signals(strategy=risk_type, n_days=(5, 14), signal='buy')

        print('Updating Sell Signals...')
        signal_checker.update_all_signals(strategy=risk_type, n_days=(5, 14), signal='sell')


if __name__ == '__main__':
    print(f'Starting Script Now: {datetime.now()}...')
    update_all_signals(results_db=results_database)
    print(f'Ending Script Now: {datetime.now()}...')
