
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
from events import OrderEvent
import json

class BTPortfolio:
    def __init__(self, events, bars,initial_capital):
        self.events = events
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.initial_capital = initial_capital

        self.current_holdings = self._create_current_holdings()
        self.holdings = self._create_holdings()
        self.current_positions = {s:0 for s in self.symbol_list}
        self.positions = self._create_positions()

        self.last_time = pd.to_datetime(self.bars.start_date)
        self.events_this_time = []

    def _create_current_holdings(self):
        d = {}
        for s in self.symbol_list:
            d[s] = 0
        d["cash"] = self.initial_capital
        d["commision"] = 0.0
        d["total"] = self.initial_capital
        return d
    def _create_holdings(self):
        d = {}
        for s in self.symbol_list:
            d[s] = 0
        d["datetime"] = self.bars.start_date
        d["cash"] = self.initial_capital
        d["commision"] = 0.0
        d["total"] = self.initial_capital
        return [d]
    def _create_positions(self):
        d = {}
        d = {s:0 for s in self.symbol_list}
        d["datetime"] = self.bars.start_date
        return [d]

    def update(self, event):
        time = self.bars.get_latest_bar(self.symbol_list[0])[0]

        dp = {s: 0 for s in self.symbol_list}
        dp["datetime"] = time
        for s in self.symbol_list:
            dp[s] = self.current_positions[s]
        self.positions.append(dp)

        d = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
        d["datetime"] = time
        d["cash"] = self.current_holdings["cash"]
        d["commision"] = self.current_holdings["commision"]
        d["total"] = self.current_holdings["cash"]
        for s in self.symbol_list:
            market_value = self.current_positions[s]*self.bars.get_latest_bar(s)[1]["close"]
            d[s] = market_value
            d["total"] += market_value
        self.holdings.append(d)
    def update_positions_from_fill(self, event):
        if event.type == "FILL":
            fill_dir = 0
            s = event.symbol
            if event.side == "BUY":
                fill_dir = 1
            elif event.side == "SELL":
                fill_dir = -1
            self.current_positions[event.symbol] += fill_dir*event.volume
    def update_holdings_from_fill(self, event):
        if event.type == "FILL":
            fill_dir = 0
            s = event.symbol
            if event.side == "BUY":
                fill_dir = 1
            elif event.side == "SELL":
                fill_dir = -1
            fill_cost = event.price
            cost = fill_cost*fill_dir*event.volume
            self.current_holdings[s] += cost
            self.current_holdings["commision"] += event.commision
            self.current_holdings["cash"] -= (cost + event.commision)
            self.current_holdings["total"] -= (cost+event.commision)
    def update_from_fill(self, event):
        if event.type == "FILL":
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)
    
    def create_equity_curve_dataframe(self):
        """
        Creates a pandas DataFrame from the all_holdings
        list of dictionaries.
        """
        curve = pd.DataFrame(self.holdings)
        curve.set_index("datetime", inplace=True)
        curve["returns"] = curve["total"].pct_change()
        curve["equity_curve"] = (1.0+curve["returns"]).cumprod()
        self.equity_curve = curve



