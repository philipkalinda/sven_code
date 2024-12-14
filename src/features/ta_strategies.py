import pandas_ta as ta

strategies = {}

default = ta.Strategy(
    name="Binance Strategy",
    description="Primary: MACD/RSI/SMA 50,200 - Secondary: BBANDS, STOCHRSI",
    ta=[
        {"kind": "sma", "length": 50},
        {"kind": "sma", "length": 200},
        {"kind": "bbands", "length": 5, "std": 2.0},
        {"kind": "rsi", "length": 14},
        {"kind": "stochrsi", "length": 14, "rsi_length": 14, "k": 3, "d": 3},
        {"kind": "macd", "fast": 12, "slow": 26, "signal": 9},
    ]
)

strategies['default'] = default
strategies['high_risk'] = default
strategies['low_risk'] = default
