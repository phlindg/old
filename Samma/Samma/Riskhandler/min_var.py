
import pandas as pd
import numpy as np
import cvxopt as opt
import cvxopt.solvers as optsolvers
import warnings

class MinVar:
    def __init__(self, events, port, recorder):
        self.events = events
        self.port = port
        self.recorder = recorder
    def min_var_portfolio(self, cov_mat, allow_short=False):
        if not isinstance(cov_mat, pd.DataFrame):
            raise ValueError("Covariance matrix is not a DataFrame")
        n = len(cov_mat)
        P = opt.matrix(cov_mat.values)
        q = opt.matrix(0.0, (n, 1))
        # Constraints Gx <= h
        if not allow_short:
            # x >= 0
            G = opt.matrix(-np.identity(n))
            h = opt.matrix(0.0, (n, 1))
        else:
            G = None
            h = None
        # Constraints Ax = b
        # sum(x) = 1
        A = opt.matrix(1.0, (1, n))
        b = opt.matrix(1.0)
        # Solve
        optsolvers.options['show_progress'] = False
        sol = optsolvers.qp(P, q, G, h, A, b)
        if sol['status'] != 'optimal':
            warnings.warn("Convergence problem")
        # Put weights into a labeled series
        weights = pd.Series(sol['x'], index=cov_mat.index)
        return weights
    def calc_vol(self,s):
        d = {}
        

    def generate_order(self, event):
        if event.type == "SIGNAL":
            order = None
            s = event.symbol
            side = event.side
            time = event.time
            price = event.price
            
            cur_quantity = self.port.current_positions[s]
            cash = self.port.current_holdings["cash"]

            


            if side == "LONG" and cur_quantity == 0:
                order = OrderEvent(time, price, s, "BUY", volume)
            elif side == "SHORT" and cur_quantity == 0:
                order = OrderEvent(time, price, s, "SELL", volume)
            elif side == "EXIT" and cur_quantity > 0:
                order = OrderEvent(time, price, s, "SELL", abs(cur_quantity))
            elif side == "EXIT" and cur_quantity < 0:
                order = OrderEvent(time, price, s, "BUY", abs(cur_quantity))
            self.events.put(order)