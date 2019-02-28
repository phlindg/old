


import numpy as np
import pandas as pd

def sharpe(returns, periods=252):
    mean = np.mean(returns)
    st = np.std(returns)
    s = np.sqrt(periods)*mean/st
    return np.float(s)
def kelly(returns):
    k = np.mean(returns)/(np.std(returns)**2)
    return k
def drawdowns(equity_curve):
    hwm = [0]
    idx = equity_curve.index
    drawdown = pd.Series(index=idx)
    duration = pd.Series(index = idx)

    for t in range(1, len(idx)):
        cur_hwm = max(hwm[t-1], equity_curve[t])
        hwm.append(cur_hwm)
        drawdown[t] = hwm[t] - equity_curve[t]
        duration[t] = 0 if drawdown[t] == 0 else duration[t-1]+1
    return drawdown, drawdown.max(), duration.max()

