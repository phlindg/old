
from events import FillEvent

class BTExe:
    def __init__(self, events):
        self.events = events
    def execute_order(self, event):
        time = event.time
        price = event.price
        symbol = event.symbol
        side = event.side
        volume = event.volume
        fill = FillEvent(time, price, symbol, side, volume)
        self.events.put(fill)

