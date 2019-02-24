import queue

from Datahandler import NasdaqCSV
from Backtest import Backtest
from Strategies import BuyHold, TS, Tripple
from Portfolio import BTPortfolio
from Riskhandler import BasicRisk
from Execution import BTExe
from Statistics import Statistics




def backtest():
    csv_dir = "C:/Users/Phili/Desktop/fond/data/"
    symbol_list = ["SAND"]
    start_date = "2006-01-03"
    train_date = "2005-01-01"
    end_date = "2019-01-03"
    initial_capital = 10000
    events = queue.Queue()
    bars = NasdaqCSV(csv_dir, symbol_list, events, start_date, train_date, end_date)
    strat = Tripple(events, bars)
    port = BTPortfolio(events, bars, initial_capital)
    risk = BasicRisk(events, port)
    exe = BTExe(events)
    stats = Statistics(port, bars)
    bt = Backtest(csv_dir, symbol_list, start_date,train_date,end_date, initial_capital,
                  events, bars, strat, port, risk, exe, stats)
    bt.initialize()
    bt.run()


