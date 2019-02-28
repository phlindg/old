
import numpy as np
import pandas as pd
from arch import arch_model

from events import SignalEvent


class TS:
    def __init__(self, events, bars,args, symbol_list=None):
        self.bars = bars
        self.events = events
        if symbol_list == None:
            self.symbol_list = self.bars.symbol_list
        else:
            self.symbol_list = symbol_list

        self.invested = {s: False for s in self.symbol_list}
        self.prices = {s: [] for s in self.symbol_list}
        self.bar_idxs = {s: 0 for s in self.symbol_list}
        print(args)
        self.lookback = int(args[0][0][0])

    def _calc_rets(self, prices):
        rets = np.diff(np.log(prices))
        return rets[~np.isnan(rets)]
    def _fit_garch11(self, rets):
        
        garch11 = arch_model(rets, mean="AR",vol='Garch', p=1, o=0, q=1, dist='Normal')

        res = garch11.fit(disp="off")
        fc = res.forecast(horizon=1).mean["h.1"].iloc[-1]
        return fc
    def calculate_signals(self, event):
        s = event.symbol
        time = event.time
        self.bar_idxs[s] += 1
        mid = (event.ask + event.bid)/2.0
        self.prices[s].append(mid)
        if self.bar_idxs[s] > self.lookback:
            rets = self._calc_rets(self.prices[s])
            fc = self._fit_garch11(rets[-self.lookback:])
            if fc > 0 and self.invested[s] == False:
                price = event.ask
                side = "LONG"
                signal = SignalEvent(time, price, s, side)
                self.events.put(signal)
                self.invested[s] = side
            elif fc > 0 and self.invested[s] == "SHORT":
                price = event.ask
                signal = SignalEvent(time, price, s, "EXIT")
                self.events.put(signal)
                self.invested[s] = False
            elif fc < 0 and self.invested[s] == False:
                price = event.bid
                side = "SHORT"
                signal = SignalEvent(time, price, s, side)
                self.events.put(signal)
                self.invested[s] = side
            elif fc < 0 and self.invested[s] == "LONG":
                price = event.bid
                signal = SignalEvent(time, price, s, "EXIT")
                self.events.put(signal)
                self.invested[s] = False



    