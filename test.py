import yfinance

msft = yfinance.Ticker('MSFT')
print(msft.info)