

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

from .performance import sharpe, drawdowns



class Statistics:
    def __init__(self, port, bars):
        self.bars = bars
        self.port = port

        self.signals = []
    def benchmark_stats(self):
        index = self.bars.index_data
        index["returns"] = index["close"].pct_change()
        index["equity_curve"] = (1+index["returns"]).cumprod()
        self.index = index
    def plot_signals(self, event):
        if event.type == "SIGNAL":
            if event.side == "LONG":
                self.signals.append(1)
            elif event.side == "SHORT":
                self.signals.append(-1)
            elif event.side == "EXIT":
                self.signals.append(0)
        elif event.type == "TICK":
            self.signals.append(0)
        
    def output_summary_stats(self):
        """s
        Creates a list of summary statistics for the portfolio.
        """
        total_return = self.port.equity_curve["equity_curve"][-1]
        self.returns = self.port.equity_curve["returns"]
        self.pnl = self.port.equity_curve["equity_curve"]
        sharpe_ratio = sharpe(self.returns, periods=252)
        self.drawdown, max_dd, dd_duration = drawdowns(self.pnl)
        self.port.equity_curve["drawdown"] = self.drawdown
        stats = {
        "Total Return": "%0.2f%%" % ((total_return - 1.0) * 100.0),
        "Return over Benchmark": "%0.2f%%" % ((total_return - self.index["equity_curve"][-1])*100),
        "Sharpe Ratio": "%0.2f" % sharpe_ratio,
        "Max Drawdown": "%0.2f%%" % (max_dd * 100.0),
        "Drawdown Duration": "%d" % dd_duration}

        return stats, max_dd, dd_duration, total_return
    def plot_stats(self):
        plt.subplot(2,3,1)
        plt.plot(self.returns)
       # plt.plot(self.index["returns"])
        plt.title("Returns")

        plt.subplot(2,3,2)
        idx = self.index["equity_curve"]
        plt.plot(idx, label="Benchmark")
        plt.plot(self.pnl, label="PnL")
        plt.legend(loc="upper right") 
        plt.title("PnL")

        plt.subplot(2,3,3)
        plt.plot(self.drawdown)
        plt.title("Drawdown")

        plt.subplot(2,3,4)
        plt.plot(self.port.equity_curve["cash"])
        plt.title("Cash")

        plt.subplot(2,3,5)
        plt.plot(self.index["returns"].rolling(252).std()*(252**0.5), label="Index vol")
        plt.plot(self.port.equity_curve["returns"].rolling(252).std()*(252**0.5), label="Strategy vol")
        plt.legend(loc="upper right")
        plt.title("Volatility")



        plt.show()


