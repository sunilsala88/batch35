
#yfinance
import yfinance as yf
import datetime as dt

e=dt.datetime.now()
s=e-dt.timedelta(days=3)
print(s,e)
data=yf.download('TSLA',start=s,end=e,multi_level_index=False,interval='1m',ignore_tz=True)

print(data)

# Plot candlestick chart using matplotlib (not mplfinance)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_candlestick(df, title='Candlestick Chart'):
	fig, ax = plt.subplots(figsize=(14, 7))
	width = 0.0008  # width for 1-minute interval, adjust as needed
	width2 = width / 3
    
	df = df.copy()
	if not isinstance(df.index, (pd.DatetimeIndex)):
		df.index = pd.to_datetime(df.index)
    
	for idx, row in df.iterrows():
		color = 'green' if row['Close'] >= row['Open'] else 'red'
		# Candle body
		ax.add_patch(
			plt.Rectangle(
				(mdates.date2num(idx) - width/2, min(row['Open'], row['Close'])),
				width,
				abs(row['Close'] - row['Open']),
				color=color,
				alpha=0.8
			)
		)
		# Wick
		ax.plot([mdates.date2num(idx), mdates.date2num(idx)], [row['Low'], row['High']], color='black', linewidth=1)
    
	ax.xaxis_date()
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
	fig.autofmt_xdate()
	ax.set_title(title)
	ax.set_ylabel('Price')
	plt.tight_layout()
	plt.show()

# Optional: resample to 5-min for clarity
import pandas as pd
df_5min = data.resample('5min').agg({
	'Open': 'first',
	'High': 'max',
	'Low': 'min',
	'Close': 'last',
	'Volume': 'sum'
})
df_5min = df_5min.dropna()
plot_candlestick(df_5min, title='TSLA 5-min Candlestick Chart')