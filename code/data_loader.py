import yfinance as yf

#DOWNLOAD AND COMPUTE YIELDS
def load_price(assets, start_date, end_date):
    data=yf.download(assets, start=start_date, end=end_date)
    price_raw=data["Close"][assets]
    print("N. of trading days:", len(price_raw))
    price=price_raw.dropna(how='any')
    print("N. of trading days with all assets:",len(price))
    print("First day of trading",price.index[0].date())
    print("Last day of trading",price.index[-1].date())
    return price

def compute_yields(price):
    return price.pct_change().dropna(how='any')