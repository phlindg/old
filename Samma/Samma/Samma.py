import queue

from Datahandler import NasdaqCSV
from Backtest import Backtest
from Strategies import BuyHold, TS, Tripple, Double, Factor
from Portfolio import BTPortfolio
from Riskhandler import BasicRisk
from Execution import BTExe
from Statistics import Statistics
from recorder import Recorder



csv_dir = "C:/Users/Phili/Desktop/fond/data/"
symbol_list = ["SAND", "ERIC", "SSAB", "VOLV", "HM"]
start_date = "2010-01-03"
train_date = "2005-01-01"
end_date = "2019-01-03"
initial_capital = 10000
events = queue.Queue()
bars = NasdaqCSV#(csv_dir, symbol_list, events, start_date, train_date, end_date)
#strat = Double#(events, bars)
port = BTPortfolio#(events, bars, initial_capital)
risk = BasicRisk#(events, port)
exe = BTExe#(events)
stats = Statistics#(port, bars)
recorder = Recorder

def backtest():

    strat = Factor
    bt = Backtest(csv_dir, symbol_list, start_date,train_date,end_date, initial_capital,
                  events, bars, strat, port, risk, exe, stats, recorder)
    bt.initialize()
    bt.run()
    bt.plot_stuff()

def opti():
    from scipy.optimize import minimize, brute
    strat = Double
    bt = Backtest(csv_dir, symbol_list, start_date,train_date,end_date, initial_capital,
                events, bars, strat, port, risk, exe, stats)
    x0 = [50,2]
    bounds = (
        (10,50),
        (2,10)
    )
    
    #best_sharpe = brute(bt.multiple_runs, ranges, args= (events, bars, symbol_list,))
    best_sharpe = minimize(bt.multiple_runs, x0 = x0, args = (events, bars, symbol_list), method="SLSQP", bounds=bounds)
    print(best_sharpe)
#opti()
backtest()