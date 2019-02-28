

import pandas as pd
import numpy as np


class Factors:
    def __init__(self):
        pass
    def RSI(self, series, period):
        series = pd.Series(series)
        delta = series.diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
        u = u.drop(u.index[:(period-1)])
        d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
        d = d.drop(d.index[:(period-1)])
        rs = u.ewm(min_periods = 0, adjust=False, com=period-1, ignore_na = False).mean() / \
            d.ewm(min_periods = 0, adjust=False, com=period-1, ignore_na = False).mean()
        rsi = 100 - 100/(1+rs)

        return rsi
    def momentum(self, series, period):
        mom = (series[-1] - series[-period])/series[-period]
        return mom
    def time_under_rsi(self, series, period, n):
        rsi = np.array(self.RSI(series, period))
        x = np.where(rsi <= n, 1.0, 0.0)
        num_days = np.sum(x)
        return num_days
    def time_over_rsi(self, series, period, n):
        rsi = np.array(self.RSI(series, period))
        x = np.where(rsi >= n, 1.0, 0.0)
        num_days = np.sum(x)
        return num_days