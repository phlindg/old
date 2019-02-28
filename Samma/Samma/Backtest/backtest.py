

from Datahandler import NasdaqCSV
from threading import Thread
from pprint import pprint
import queue
import numpy as np

class Backtest:
    def __init__(self,csv_dir, symbol_list,start_date, train_date, end_date, initial_capital,
                events, bars_cls, strategy_cls, port_cls, risk_cls, exe_cls, statistics_cls, recorder_cls):
        self.events = events
        self.bars_cls = bars_cls
        self.strategy_cls = strategy_cls
        self.port_cls = port_cls
        self.risk_cls = risk_cls
        self.exe_cls = exe_cls
        self.statistics_cls = statistics_cls
        self.recorder_cls = recorder_cls

        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.start_date = start_date
        self.train_date = train_date
        self.end_date = end_date
        self.initial_capital = initial_capital

    def initialize(self, *args):
        self.bars = self.bars_cls(self.csv_dir, self.symbol_list,self.events, self.start_date, self.train_date, self.end_date)
        self.strat = self.strategy_cls(self.events, self.bars, args)
        self.port = self.port_cls(self.events, self.bars, self.initial_capital)
        self.recorder = self.recorder_cls(self.events, self.bars)
        self.risk = self.risk_cls(self.events, self.port, self.recorder)
        self.exe = self.exe_cls(self.events)
        self.stats = self.statistics_cls(self.port, self.bars)
        
    def trade(self):
        while True:
            if self.bars.continue_backtest == True:
                self.bars.update_bars()
            else:
                
                break
            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event.type == "MARKET":
                        self.port.update(event)
                    elif event.type == "TICK":
                        self.strat.calculate_signals(event)
                        self.recorder.store_tick(event)
                    elif event.type == "SIGNAL":
                        self.risk.generate_order(event)
                    elif event.type == "ORDER":
                        self.exe.execute_order(event)
                    elif event.type == "FILL":
                        self.port.update_from_fill(event)
                    self.stats.plot_signals(event)

    def tick_to_queue(self):
        while True:
            self.bars.update_bars()
    def run(self):
        #ticks = Thread(target=self.tick_to_queue, daemon = True)
        #trade = Thread(target=self.trade, daemon=True)
        #ticks.start()
        #trade.start()
        self.trade()
        self.port.create_equity_curve_dataframe()
        self.stats.benchmark_stats()
        stats, max_dd, dd_duration, total_return = self.stats.output_summary_stats()
        return stats, max_dd, dd_duration, total_return

        
    def plot_stuff(self):
        self.stats.plot_stats()
    def multiple_runs(self, *args):
        self.initialize(args)
        stats, max_dd, dd_duration, total_return = self.run()
        val = max_dd + dd_duration - total_return
        return val



    