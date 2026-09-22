import pandas as pd
import numpy as np

def return_annual(serie):
    return serie.mean()*252

def volatility_annual(serie):
    return serie.std()*np.sqrt(252)

def sharpe_ratio(serie,rf):
    return(return_annual(serie)-rf)/volatility_annual(serie)

def var_95_daily(serie):
    return serie.quantile(0.05)

def cvar_95_daily(serie):
    var = var_95_daily(serie)
    return serie[serie <= var].mean()

def equity_curve(serie):
    return (1+serie).cumprod()

def drawdown(ec):
    max_value=ec.cummax()
    dd=(ec-max_value)/max_value
    return dd

def metrics(serie, rf):
    return {
        "Return":     return_annual(serie),
        "Volatility": volatility_annual(serie),
        "Sharpe":     sharpe_ratio(serie, rf),
        "VaR 95% daily":var_95_daily(serie),
        "CVaR 95% daily":cvar_95_daily(serie)
        }