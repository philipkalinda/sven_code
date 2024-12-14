## Technical Analysis Strategy

#### 1. Moving Averages
- purchasing in bullish period
- selling in bearish periods  


#### 2. RSI
- purchasing coming out of the thresholds
- sell and buy signal just as the RSI stops indicating


#### 3. MACD
- At the crossover, the standard deviation from the MACD line
- Normalise by mean? - that way we consider the skew
- Or use deviation from 0
- look at minimum point since being above or below centre line


#### 4. Stochastic RSI
- seems too sensitive - may leave out


#### 5. Bollinger Bands
- TBD


#### 6. Regression 
- to extrapolate a bit for sma crossover if not in bullish/bearish period
- extrapolate to next 30 days
- and gradient of faster SMA is steeper (or how much sooner in the next 30 days)





## Strategy

1. Approach... Use MACD to init a signal, verify with RSI
    1. if yes, make trade signal
    2. if no from RSI:
        1. extrapolate crossovers from SMAs and detect within 30 days
        2. check stochastic RSI exit/enter signal to trade in last 30 days
        3. check bollinger band volatility in period
        4. if yes to all, make trade signal
    3. else no trade signal