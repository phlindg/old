
import numpy as np
from events import OrderEvent


class BasicRisk:
    def __init__(self, events, port):
        self.events = events
        self.port = port

    def generate_order(self, event):
        if event.type == "SIGNAL":
            order = None
            s = event.symbol
            side = event.side
            time = event.time
            price = event.price
            
            cur_quantity = self.port.current_positions[s]
            cash = self.port.current_holdings["cash"]

            volume = min(100,cash/(len(self.port.symbol_list)*price))


            if side == "LONG" and cur_quantity == 0:
                order = OrderEvent(time, price, s, "BUY", volume)
            elif side == "SHORT" and cur_quantity == 0:
                order = OrderEvent(time, price, s, "SELL", volume)
            elif side == "EXIT" and cur_quantity > 0:
                order = OrderEvent(time, price, s, "SELL", abs(cur_quantity))
            elif side == "EXIT" and cur_quantity < 0:
                order = OrderEvent(time, price, s, "BUY", abs(cur_quantity))
            self.events.put(order)
