
class MarketEvent:
    def __init__(self):
        self.type="MARKET"
class TickEvent:
    def __init__(self, time, bid, ask, symbol):
        self.type = "TICK"
        self.time = time
        self.bid = bid
        self.ask = ask
        self.symbol = symbol

class SignalEvent:
    def __init__(self, time, price, symbol,side):
        self.type = "SIGNAL"
        self.time = time
        self.price = price
        self.symbol = symbol
        self.side = side
class OrderEvent:
    def __init__(self, time, price, symbol, side, volume):
        self.type = "ORDER"
        self.time = time
        self.price = price
        self.symbol = symbol
        self.side = side
        self.volume = volume
class FillEvent:
    def __init__(self, time, price, symbol, side, volume, commision =None):
        self.type = "FILL"
        self.time = time
        self.price = price
        self.symbol = symbol
        self.side = side
        self.volume = volume
        if commision == None:
            self.commision = self.calculate_commision(self.volume, self.price)
        else:
            self.commision = commision
    def calculate_commision(self, volume, price):
        comm = volume*price*0.0025
        return min(comm, 1)