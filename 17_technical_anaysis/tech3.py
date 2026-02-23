
from __future__ import annotations

from typing import Any, Optional

import numpy as np
import pandas as pd
import yfinance as yf
import mplfinance as mpf


def _ma(mode: str, series: pd.Series, period: int) -> pd.Series:
	mode = mode.lower()
	if mode == "ema":
		return series.ewm(span=period, adjust=False, min_periods=period).mean()
	if mode == "sma":
		return series.rolling(window=period, min_periods=period).mean()
	if mode == "wma":
		weights = np.arange(1, period + 1, dtype=float)

		def _weighted(arr: np.ndarray) -> float:
			return float(np.dot(arr, weights) / weights.sum())

		return series.rolling(window=period, min_periods=period).apply(
			_weighted, raw=True
		)
	# Default to RMA
	return series.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()


def _true_range(
	high: pd.Series,
	low: pd.Series,
	close: pd.Series,
	drift: int,
	set_prenan: bool,
) -> pd.Series:
	prev_close = close.shift(drift)
	tr_components = pd.concat(
		[(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1
	)
	tr = tr_components.max(axis=1)
	if set_prenan:
		tr.iloc[:drift] = np.nan
	return tr


def atr(
	high: pd.Series,
	low: pd.Series,
	close: pd.Series,
	length: Optional[int] = None,
	mamode: Optional[str] = None,
	talib: Optional[bool] = None,
	prenan: Optional[bool] = None,
	drift: Optional[int] = None,
	offset: Optional[int] = None,
	**kwargs: Any,
) -> pd.Series:
	if length is None or int(length) <= 0:
		length = 14
	else:
		length = int(length)

	required_len = length + 1
	if any(series is None for series in (high, low, close)):
		raise ValueError("high, low, and close must be valid pandas Series.")
	if min(len(high), len(low), len(close)) < required_len:
		raise ValueError(
			f"Input series must each contain at least {required_len} rows."
		)

	mamode = "rma" if mamode is None else str(mamode).lower()
	mode_talib = True if talib is None else bool(talib)
	prenan = False if prenan is None else bool(prenan)
	drift = 1 if drift is None else max(int(drift), 1)
	offset = 0 if offset is None else int(offset)

	if mode_talib:
		try:
			from talib import ATR as TA_ATR  # type: ignore

			atr_series = pd.Series(
				TA_ATR(high.values, low.values, close.values, timeperiod=length),
				index=close.index,
			)
		except Exception:
			tr = _true_range(high, low, close, drift, prenan)
			if tr.isna().all():
				return
			presma = kwargs.pop("presma", True)
			if presma:
				sma_nth = tr.iloc[0:length].mean()
				tr.iloc[: length - 1] = np.nan
				tr.iloc[length - 1] = sma_nth
			atr_series = _ma(mamode, tr, period=length)
	else:
		tr = _true_range(high, low, close, drift, prenan)
		if tr.isna().all():
			return
		presma = kwargs.pop("presma", True)
		if presma:
			sma_nth = tr.iloc[0:length].mean()
			tr.iloc[: length - 1] = np.nan
			tr.iloc[length - 1] = sma_nth
		atr_series = _ma(mamode, tr, period=length)

	if atr_series.isna().all():
		return

	percent = bool(kwargs.pop("percent", False))
	if percent:
		atr_series = atr_series * (100 / close)

	if offset != 0:
		atr_series = atr_series.shift(offset)

	if "fillna" in kwargs:
		atr_series = atr_series.fillna(kwargs["fillna"])

	atr_series.name = f"ATR{mamode[0]}{'p' if percent else ''}_{length}"
	atr_series.attrs["category"] = "volatility"
	return atr_series


def supertrend(
	high: pd.Series,
	low: pd.Series,
	close: pd.Series,
	length: Optional[int] = None,
	atr_length: Optional[int] = None,
	multiplier: Optional[float] = None,
	atr_mamode: Optional[str] = None,
	offset: Optional[int] = None,
	**kwargs: Any,
) -> pd.DataFrame:
	if length is None or int(length) <= 0:
		length = 7
	else:
		length = int(length)

	atr_length = length if atr_length is None else int(atr_length)

	min_len = length + 1
	if any(series is None for series in (high, low, close)):
		raise ValueError("high, low, and close must be valid pandas Series.")
	if min(len(high), len(low), len(close)) < min_len:
		raise ValueError(
			f"Input series must each contain at least {min_len} rows."
		)

	multiplier = 3.0 if multiplier is None else float(multiplier)
	atr_mamode = "rma" if atr_mamode is None else str(atr_mamode).lower()
	offset = 0 if offset is None else int(offset)

	hl2 = (high + low) / 2.0
	atr_series = atr(high, low, close, atr_length, mamode=atr_mamode)
	if atr_series is None:
		return

	m = close.size
	dir_vals = [1] * m
	trend = [0.0] * m
	long_vals = [np.nan] * m
	short_vals = [np.nan] * m

	lb = hl2 - multiplier * atr_series
	ub = hl2 + multiplier * atr_series

	for i in range(1, m):
		if close.iat[i] > ub.iat[i - 1]:
			dir_vals[i] = 1
		elif close.iat[i] < lb.iat[i - 1]:
			dir_vals[i] = -1
		else:
			dir_vals[i] = dir_vals[i - 1]
			if dir_vals[i] > 0 and lb.iat[i] < lb.iat[i - 1]:
				lb.iat[i] = lb.iat[i - 1]
			if dir_vals[i] < 0 and ub.iat[i] > ub.iat[i - 1]:
				ub.iat[i] = ub.iat[i - 1]

		if dir_vals[i] > 0:
			trend[i] = long_vals[i] = lb.iat[i]
		else:
			trend[i] = short_vals[i] = ub.iat[i]

	trend[0] = np.nan
	dir_vals[:length] = [np.nan] * length

	props = f"_{length}_{multiplier}"
	data = {
		f"SUPERT{props}": trend,
		f"SUPERTd{props}": dir_vals,
		f"SUPERTl{props}": long_vals,
		f"SUPERTs{props}": short_vals,
	}
	df = pd.DataFrame(data, index=close.index)
	df.name = f"SUPERT{props}"
	df.attrs["category"] = "overlap"

	if offset != 0:
		df = df.shift(offset)

	if "fillna" in kwargs:
		df.fillna(kwargs["fillna"], inplace=True)

	return df


data=yf.download('TSLA',period='5y',multi_level_index=False)
print(data)

#sma
data['sma']=data['Close'].rolling(window=5, min_periods=5).mean()

super1 = supertrend(data['High'], data['Low'], data['Close'], length=7, multiplier=3.0)
print(super1)

superl=mpf.make_addplot(super1['SUPERTl_7_3.0'],color='green')
supers=mpf.make_addplot(super1['SUPERTs_7_3.0'],color='red')

mpf.plot(data,type='candle',  style='yahoo',addplot=[superl,supers])
