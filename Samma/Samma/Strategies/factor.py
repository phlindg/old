


from events import SignalEvent
from Statistics import Factors

import pandas as pd
import numpy as np


class Factor:
    def __init__(self, events, bars, args, symbol_list = None):
        self.events = events
        self.bars = bars
        if symbol_list == None:
            self.symbol_list = self.bars.symbol_list
        else:
            self.symbol_list = symbol_list

        self.invested = {s: False for s in self.symbol_list}
        self.prices = {s: [] for s in self.symbol_list}
        self.bar_index = {s: 0 for s in self.symbol_list}
    def get_factors(self, prices):
        facts = {}
        f = Factors()
        
        temp = {}
        temp["RSI"] = f.RSI(prices, 14)
        temp["Momentum"] = f.momentum(prices, 14)
        
        return temp
    def calculate_signals(self, event):
        s = event.symbol
        time = event.time
        self.bar_index[s] += 1
        mid = (event.bid + event.ask)/2.0
        self.prices[s].append(mid)
        if self.bar_index[s] > 15:
            facts = self.get_factors(self.prices[s])
            print(facts)
            rsi = facts["RSI"].iloc[-1]
            momentum = facts["Momentum"]
            if rsi < 50 and momentum > 0 and self.invested[s] == False:
                price = event.ask
                side ="LONG"
                signal = SignalEvent(time, price, s, side)
                self.events.put(signal)
                self.invested[s] = side
            elif rsi > 50 and momentum < 0 and self.invested[s] == "LONG":
                price = event.bid
                signal = SignalEvent(time, price, s, "EXIT")
                self.events.put(signal)
                self.invested[s] = False

