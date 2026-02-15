
#yfinance
import yfinance as yf
import datetime as dt

e=dt.datetime.now()
s=e-dt.timedelta(days=3)

print(s, e)
data = yf.download('TSLA', start=s, end=e, multi_level_index=False, interval='1m', ignore_tz=True)

print(data)

# Plot candlestick chart using Plotly
import plotly.graph_objects as go

if not data.empty:
	fig = go.Figure(data=[
		go.Candlestick(
			x=data.index,
			open=data['Open'],
			high=data['High'],
			low=data['Low'],
			close=data['Close']
		)
	])
	fig.update_layout(
		title='TSLA 1-Minute Candlestick Chart',
		xaxis_title='Time',
		yaxis_title='Price (USD)',
		xaxis_rangeslider_visible=False
	)
	fig.show()
else:
	print('No data to plot.')
