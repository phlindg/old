



class Recorder:
    def __init__(self, events, bars):
        self.events = events
        self.bars = bars
        self.symbol_list = self.bars.symbol_list


        self.ticks = {s: [] for s in self.symbol_list}
    def store_tick(self, event):
        if event.type == "TICK":
            s = event.symbol
            time = event.time
            bid = event.bid
            ask = event.ask
            tup = (time, bid, ask)
            self.ticks[s].append(tup)
