import pandas as pd
import numpy as np
from scipy.optimize import minimize

#EQUAL WEIGHTS
def compute_equal_weights(assets):
    equal_weights=pd.Series(1/len(assets),index=assets)
    return equal_weights

#MARKOWITZ
def sharpe_ratio(w,rf,y_mean,cov_matrix):
    pf_yields=w@y_mean
    pf_volatility=np.sqrt(w@cov_matrix@w)
    return (pf_yields-rf)/pf_volatility

def negative_sharpe_ratio(w, rf, y_mean, cov_matrix):
    return -sharpe_ratio(w, rf, y_mean, cov_matrix)


def weights_markowitz(rf, y_mean, cov_matrix):
    if y_mean.max()<=rf:
        raise ValueError("No asset yield higher than risk-free")
    n = len(y_mean)
    w0 = np.ones(n) / n
    bounds = [(0, 1)] * n
    constraint = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    result = minimize(negative_sharpe_ratio, w0, args=(rf, y_mean, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraint)

    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")
    
    assert np.isclose(np.sum(result.x), 1.0), "Markowitz weights don't sum to 1"

    return pd.Series(result.x, index=y_mean.index)


#RISK PARITY
def risk_contributions(w,cov_matrix):
    pf_volatility=np.sqrt(w@cov_matrix@w)
    rc=w*(cov_matrix@w)/pf_volatility
    return rc

def objective_risk_parity(w,cov_matrix):
    rc=risk_contributions(w,cov_matrix)
    target=np.mean(rc)
    return np.sum(((rc-target)/target)**2)



def weights_risk_parity(cov_matrix):
    n=len(cov_matrix)
    w0=np.ones(n)/n
    bounds = [(0, 1)] * n
    constraint = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    result = minimize(objective_risk_parity, w0, args=(cov_matrix,), method='SLSQP', bounds=bounds, constraints=constraint)
    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")
    assert np.isclose(np.sum(result.x),1.0), "Risk parity weights don't sum to 1"
    return pd.Series(result.x, index=cov_matrix.index)