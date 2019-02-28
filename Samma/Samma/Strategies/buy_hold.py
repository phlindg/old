

import numpy as np
from events import SignalEvent

class BuyHold:
    def __init__(self, events, bars, symbol_list = None):
        self.events = events
        self.bars = bars
        if symbol_list == None:
            self.symbol_list = self.bars.symbol_list
        else:
            self.symbol_list = symbol_list

        self.invested = {s: False for s in self.symbol_list}
    def calculate_signals(self, event):
        s = event.symbol
        time = event.time
        if self.invested[s] == False:
            price = event.ask
            side = "LONG"
            signal = SignalEvent(time, price, s, side)
            self.events.put(signal)
            self.invested[s] = "LONG"
            print(side + " on "+s)


