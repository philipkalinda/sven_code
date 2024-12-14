config = {}

default = {
    #SMA
    'sma_lookback': 5, # days to look back to forecast
    'sma_crossover_forecast': 30, # days ahead to look for crossover
    #MACD
    'macd_days_to_calc_std': 200, # days worth of previous data to calculate the std
    'macd_std': 2, # number of std to go past to init trading signal
    #RSI
    'rsi_lookback': 30, # number of days to look back if there has been an RSI signal detect
    'rsi_upper_threshold': 80, # RSI upper threshold
    'rsi_lower_threshold': 20, # RSI lower threshold
    #StochRSI
    'stoch_rsi_lookback': 15, # number of days to look back if there is a stochastic RSI signal
    'stoch_rsi_upper_threshold': 95, # Stochastic RSI upper threshold
    'stoch_rsi_lower_threshold': 5, # Stochastic RSI lower threshold
    #BBANDS
    'bbands_days_to_calc_std': 200, # days worth of previous data to calculate the std
    'bbands_diff_std': 3 # number of std to go past to accept alternate trading signal
}

low_risk = {
#SMA
    'sma_lookback': 20, # days to look back to forecast
    'sma_crossover_forecast': 20, # days ahead to look for crossover
    #MACD
    'macd_days_to_calc_std': 250, # days worth of previous data to calculate the std
    'macd_std': 2.5, # number of std to go past to init trading signal
    #RSI
    'rsi_lookback': 20, # number of days to look back if there has been an RSI signal detect
    'rsi_upper_threshold': 90, # RSI upper threshold
    'rsi_lower_threshold': 10, # RSI lower threshold
    #StochRSI
    'stoch_rsi_lookback': 15, # number of days to look back if there is a stochastic RSI signal
    'stoch_rsi_upper_threshold': 97.5, # Stochastic RSI upper threshold
    'stoch_rsi_lower_threshold': 2.5, # Stochastic RSI lower threshold
    #BBANDS
    'bbands_days_to_calc_std': 250, # days worth of previous data to calculate the std
    'bbands_diff_std': 3.5 # number of std to go past to accept alternate trading signal
}

high_risk = {
#SMA
    'sma_lookback': 5, # days to look back to forecast
    'sma_crossover_forecast': 45, # days ahead to look for crossover
    #MACD
    'macd_days_to_calc_std': 100, # days worth of previous data to calculate the std
    'macd_std': 1.5, # number of std to go past to init trading signal
    #RSI
    'rsi_lookback': 45, # number of days to look back if there has been an RSI signal detect
    'rsi_upper_threshold': 70, # RSI upper threshold
    'rsi_lower_threshold': 30, # RSI lower threshold
    #StochRSI
    'stoch_rsi_lookback': 15, # number of days to look back if there is a stochastic RSI signal
    'stoch_rsi_upper_threshold': 90, # Stochastic RSI upper threshold
    'stoch_rsi_lower_threshold': 10, # Stochastic RSI lower threshold
    #BBANDS
    'bbands_days_to_calc_std': 100, # days worth of previous data to calculate the std
    'bbands_diff_std': 2.5 # number of std to go past to accept alternate trading signal
}

# config['default'] = default
# config['low_risk'] = low_risk
config['high_risk'] = high_risk