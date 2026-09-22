import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import data_loader as dl
import allocations as al
import compute_metrics as cm

#ASSETS TICKERS
assets=["SPY","GLD","TLT","VNQ"]

#IN SAMPLE DATES
start_date="2015-01-01"
end_date="2019-01-01"

#STRESS TEST DATES
start_stress="2020-01-01"
end_stress="2021-01-01"

#RISK FREE
rf=0.02

#FIGURES SAVE DIRECTORY
figures_path=Path(__file__).resolve().parent.parent/"figures"
figures_path.mkdir(exist_ok=True)


#IN SAMPLE DATAS
price=dl.load_price(assets,start_date,end_date)
y_assets=dl.compute_yields(price)
y_mean_annual=y_assets.mean()*252
cov_matrix=y_assets.cov()*252

#WEIGHTS
w_equal=al.compute_equal_weights(assets)
w_markowitz=al.weights_markowitz(rf,y_mean_annual,cov_matrix)
w_riskparity=al.weights_risk_parity(cov_matrix)

weights=pd.DataFrame({"Equal":w_equal,"Markowitz":w_markowitz,"Risk Parity":w_riskparity})
print("Strategies Weights")
print(weights)

#RISK CONTRIBUTIONS
rc_table=pd.DataFrame({name:al.risk_contributions(weights[name],cov_matrix)for name in weights})
rc_table=rc_table/rc_table.sum()
print("Risk Contributions")
print(rc_table)

#PORTFOLIO, EQUITY CURVE, DRAWDOWN
portfolios=y_assets@weights
ec_sample=cm.equity_curve(portfolios)
dd_sample=cm.drawdown(ec_sample)

#STRESS TEST DDOWNLOAD-PORTOFOLIO-EQUITY CURVE-DRAWDOWN
price_stress=dl.load_price(assets,start_stress,end_stress)
y_stress=dl.compute_yields(price_stress)

portfolios_stress=y_stress@weights
ec_stress=cm.equity_curve(portfolios_stress)
dd_stress=cm.drawdown(ec_stress)

#RESULTS
table_sample=pd.DataFrame({name:cm.metrics(portfolios[name],rf) for name in portfolios})
table_sample.loc["Max DD"]=dd_sample.min()
table_stress=pd.DataFrame({name:cm.metrics(portfolios_stress[name],rf) for name in portfolios_stress})
table_stress.loc["Max DD"]=dd_stress.min()

print("In Sample Results")
print(table_sample)
print("Stress Test Results")
print(table_stress)

#EQUITY CURVE PLOTS
ec_sample.plot(title="Equity Curve In Sample")
plt.ylabel("Equity Curve")
plt.savefig(figures_path/"equity_curve_2015_2018.png", dpi=150, bbox_inches="tight")
plt.close()

ec_stress.plot(title="Equity Curve Stress Test")
plt.ylabel("Equity Curve")
plt.savefig(figures_path/"equity_curve_2020.png", dpi=150, bbox_inches="tight")
plt.close()

#DRAWDOWN PLOTS
dd_sample.plot(title="Drawdown In Sample")
plt.ylabel("Drawdown")
plt.savefig(figures_path/"drawdown_2015_2018.png", dpi=150, bbox_inches="tight")
plt.close()

dd_stress.plot(title="Drawdown Stress Test")
plt.ylabel("Drawdown")
plt.savefig(figures_path/"drawdown_2020.png", dpi=150, bbox_inches="tight")
plt.close()