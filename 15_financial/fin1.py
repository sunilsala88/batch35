
#yfinance
import yfinance as yf

data=yf.download('TSLA',start='2024-01-01',end='2024-12-31',multi_level_index=False)
print(data)
