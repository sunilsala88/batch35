
import numpy as np
import pandas as pd
import yfinance as yf
import mplfinance as mpf


data=yf.download('TSLA',period='5y',multi_level_index=False)
print(data)


def doji(data, threshold=0.01):
    """
    Detect Doji candlestick patterns in OHLC data.
    A Doji occurs when the open and close prices are virtually equal,
    meaning the body is very small relative to the full candle range.

    Parameters:
        data: DataFrame with Open, High, Low, Close columns
        threshold: max ratio of body size to candle range (default 0.01 = 1%)

    Returns:
        DataFrame with a 'Doji' column (True/False) and filtered doji rows printed.
    """
    df = data.copy()
    body = abs(df['Close'] - df['Open'])
    candle_range = df['High'] - df['Low']

    # Avoid division by zero for flat candles
    is_doji = (body <= (candle_range * threshold)) & (candle_range != 0)

    df['Doji'] = np.where(is_doji, 1, np.nan)

    doji_days = df[df['Doji'] == 1]
    print(f"\nTotal Doji patterns found: {len(doji_days)}\n")
    print(doji_days[['Open', 'High', 'Low', 'Close', 'Doji']])
    return df['Doji']


d = doji(data)
# d=d*data['High']
print(d)



d=mpf.make_addplot(d,color='black',type='scatter',markersize=5)


mpf.plot(data,type='candle',  style='yahoo',addplot=[d])