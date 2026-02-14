
#yfinance
import yfinance as yf
data=yf.download('EURUSD=X',period='5y',multi_level_index=False)
print(data)