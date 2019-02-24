



import numpy as np
from events import SignalEvent

class Tripple:
    def __init__(self, events, bars, symbol_list = None):
        self.events = events
        self.bars = bars
        if symbol_list == None:
            self.symbol_list = self.bars.symbol_list
        else:
            self.symbol_list = symbol_list

        self.prices = {s:[] for s in self.symbol_list}
      

        self.long_window = 15
        self.middle_window = 10
        self.short_window = 5

        self.invested = {s: False for s in self.symbol_list}
        self.bar_idxs = {s: 0 for s in self.symbol_list}
    def moving_average(self,a, n=3) :
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n
    def calculate_signals(self, event):
        
        s = event.symbol
        self.bar_idxs[s] += 1
        time = event.time
        mid_price = (event.bid + event.ask)/2.0
        self.prices[s].append(mid_price)
        if self.bar_idxs[s] > self.long_window:
            long_avg = self.moving_average(self.prices[s], self.long_window)[-1]
            middle_avg = self.moving_average(self.prices[s], self.middle_window)[-1]
            short_avg = self.moving_average(self.prices[s], self.short_window)[-1]
            print(long_avg, middle_avg, short_avg)
            if long_avg < middle_avg and middle_avg < short_avg and self.invested[s] == False:
                price = event.ask
                side = "LONG"
                signal = SignalEvent(time, price, s,side)
                self.events.put(signal)
                self.invested[s] = side
            elif long_avg > middle_avg and middle_avg > short_avg and self.invested[s] == False:
                price = event.bid
                side = "SHORT"
                signal = SignalEvent(time, price, s,side)
                self.events.put(signal)
                self.invested[s] = side
            elif (long_avg > middle_avg and middle_avg < short_avg) or (long_avg < middle_avg and middle_avg > short_avg):
                if self.invested[s] == "SHORT":
                    price = event.ask
                    signal = SignalEvent(time, price, s,"EXIT")
                    self.events.put(signal)
                    self.invested[s] = False
                elif self.invested[s] == "LONG":
                    price = event.bid
                    signal = SignalEvent(time, price, s,"EXIT")
                    self.events.put(signal)
                    self.invested[s] = False
       



