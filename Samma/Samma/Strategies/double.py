



import numpy as np
from events import SignalEvent

class Double:
    def __init__(self, events, bars, args, symbol_list = None):
        self.events = events
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
       
        print(self.symbol_list)
        self.invested = {s: False for s in self.symbol_list}
        self.long_window = int(args[0][0][0])
        self.short_window = int(args[0][0][1])
        self.bar_indexs = {s: 0 for s in self.symbol_list}
        self.prices = {s: [] for s in self.symbol_list}

    def moving_average(self,a, n=3) :
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def calculate_signals(self, event):
        if event.type == "TICK":
            
            
                
                
            s = event.symbol
            self.bar_indexs[s] += 1
            time = event.time
            mid = (event.bid + event.ask)/2.0
            self.prices[s].append(mid)
            
            
            if self.bar_indexs[s] >= self.long_window:
                long_avg = self.moving_average(self.prices[s], n = self.long_window)[-1]
                short_avg = self.moving_average(self.prices[s], n = self.short_window)[-1]
                if short_avg < long_avg:
                    if self.invested[s] == False:
                        price = event.ask
                        signal = SignalEvent(time, price, s, "LONG")
                        self.events.put(signal)
                        self.invested[s] = "LONG"
                    elif self.invested == "SHORT":
                        price = event.bid
                        signal = SignalEvent(time, price, s, "EXIT")
                        self.events.put(signal)
                        self.invested[s] = False
                elif short_avg > long_avg:
                    if self.invested[s] == False:
                        price = event.bid
                        signal = SignalEvent(time, price, s, "SHORT")
                        self.events.put(signal)
                        self.invested[s] = "SHORT"
                    elif self.invested[s] == "LONG":
                        price = event.ask
                        signal = SignalEvent(time, price, s, "EXIT")
                        self.events.put(signal)
                        self.invested[s] = False                     


                        

