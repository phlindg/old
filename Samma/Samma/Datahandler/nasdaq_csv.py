
import os

import numpy as np
import pandas as pd

from events import MarketEvent, TickEvent


class NasdaqCSV:
    def __init__(self, csv_dir, symbol_list, events,start_date,train_date, end_date):
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.start_date = start_date
        self.train_date = train_date
        self.end_date = end_date
        

        self.events = events


        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.training_data = {}
        self.continue_backtest = True

        self._open_convert_csv_files()
        

    def _open_convert_csv_files(self):
        comb_index = None
        self.index_data = pd.read_csv(
            os.path.join(self.csv_dir, "OMXS30.csv"),
            index_col = 0, header=0,names=["datetime","close"],parse_dates=True, sep=";").ix[::-1]
                         
        for s in self.symbol_list:
            self.symbol_data[s] = pd.read_csv(
                os.path.join(self.csv_dir, "%s.csv" % s),
                header = 0, index_col = 0, parse_dates = True,
                names= ["datetime", "bid","ask","open", "high", "low", "close", "avg_price", "volume", "turnover", "trades"],
                sep = ";"
                ).ix[::-1]
            self.latest_symbol_data[s] = []
        self.index_data = self.index_data.loc[self.start_date:self.end_date]
        for s in self.symbol_list:
            self.training_data[s] = self.symbol_data[s].loc[self.train_date:self.start_date]
            self.symbol_data[s] = self.symbol_data[s].loc[self.start_date:self.end_date]
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index.union(self.symbol_data[s].index)
            self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index, method="pad").iterrows()
    def _get_new_bar(self, symbol):
        for b in self.symbol_data[symbol]:
            yield b
    def get_latest_bar(self, symbol):
        return self.latest_symbol_data[symbol][-1]
    def get_latest_datetime(self):
        return self.latest_symbol_data[self.symbol_list[0]][-1][0]
    def update_bars(self):
        for s in self.symbol_list:
            try:
                bar = next(self._get_new_bar(s))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
                    ask = bar[1]["ask"]
                    bid = bar[1]["bid"]
                    time = bar[0]
                    tick = TickEvent(time, bid, ask, s)
                    self.events.put(tick)
        self.events.put(MarketEvent())
