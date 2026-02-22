from __future__ import annotations

from typing import Any, Optional

import numpy as np
import pandas as pd
import yfinance as yf
import mplfinance as mpf

def willr(
	high: pd.Series,
	low: pd.Series,
	close: pd.Series,
	length: Optional[int] = None,
	talib: Optional[bool] = None,
	offset: Optional[int] = None,
	**kwargs: Any,
) -> pd.Series:
	"""William's Percent R

	This indicator attempts to identify "overbought" and "oversold"
	conditions similar to the RSI.

	Sources:
		* [tradingview](https://www.tradingview.com/wiki/Williams_%25R_(%25R))

	Parameters:
		high (Series): ``high`` Series
		low (Series): ``low`` Series
		close (Series): ``close`` Series
		length (int): The period. Default: ``14``
		talib (bool): If installed, use TA Lib. Default: ``True``
		offset (int): Post shift. Default: ``0``

	Other Parameters:
		fillna (value): ``pd.Series.fillna(value)``
		min_periods (int): Minimum observations in window. Default: ``length``

	Returns:
		Series: 1 column
	"""
	if length is None or int(length) <= 0:
		length = 14
	else:
		length = int(length)

	if "min_periods" in kwargs and kwargs["min_periods"] is not None:
		min_periods = int(kwargs["min_periods"])
	else:
		min_periods = length

	required_len = max(length, min_periods)
	if any(series is None for series in (high, low, close)):
		raise ValueError("high, low, and close must be valid pandas Series.")
	if min(len(high), len(low), len(close)) < required_len:
		raise ValueError(
			f"Input series must each contain at least {required_len} rows."
		)

	mode_talib = True if talib is None else bool(talib)
	offset = 0 if offset is None else int(offset)

	if mode_talib:
		try:
			from talib import WILLR  # type: ignore

			result = WILLR(high.values, low.values, close.values, timeperiod=length)
			willr_series = pd.Series(result, index=close.index)
		except Exception:
			lowest_low = low.rolling(length, min_periods=min_periods).min()
			highest_high = high.rolling(length, min_periods=min_periods).max()
			willr_series = 100 * (
				(close - lowest_low) / (highest_high - lowest_low) - 1
			)
	else:
		lowest_low = low.rolling(length, min_periods=min_periods).min()
		highest_high = high.rolling(length, min_periods=min_periods).max()
		willr_series = 100 * ((close - lowest_low) / (highest_high - lowest_low) - 1)

	if offset != 0:
		willr_series = willr_series.shift(offset)

	if "fillna" in kwargs:
		willr_series = willr_series.fillna(kwargs["fillna"])

	willr_series.name = f"WILLR_{length}"
	willr_series.attrs["category"] = "momentum"
	return willr_series


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
	"""Average True Range

	This indicator attempts to quantify volatility with a focus on gaps or
	limit moves.

	Sources:
		* [tradingview](https://www.tradingview.com/wiki/Average_True_Range_(ATR))

	Parameters:
		high (Series): ``high`` Series
		low (Series): ``low`` Series
		close (Series): ``close`` Series
		length (int): The period. Default: ``14``
		mamode (str): Moving average mode. Default: ``"rma"``
		talib (bool): If installed, use TA Lib. Default: ``True``
		prenan (bool): Sets initial true-range values to ``np.nan`` based on
			``drift``. Default: ``False``
		drift (int): Difference amount. Default: ``1``
		offset (int): Post shift. Default: ``0``

	Other Parameters:
		percent (bool): Return as percent. Default: ``False``
		fillna (value): ``pd.Series.fillna(value)``

	Returns:
		Series: 1 column
	"""
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

	def _true_range(
		high_s: pd.Series,
		low_s: pd.Series,
		close_s: pd.Series,
		drift_n: int,
		set_prenan: bool,
	) -> pd.Series:
		prev_close = close_s.shift(drift_n)
		tr_components = pd.concat(
			[(high_s - low_s), (high_s - prev_close).abs(), (low_s - prev_close).abs()],
			axis=1,
		)
		tr = tr_components.max(axis=1)
		if set_prenan:
			tr.iloc[:drift_n] = np.nan
		return tr

	def _ma(mode: str, series: pd.Series, period: int) -> pd.Series:
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
		return series.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()

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

data=yf.download('TSLA',start='2023-01-01',end='2023-12-31',multi_level_index=False,interval='1d',ignore_tz=True)
print(data)

data['SMA'] = data['Close'].rolling(window=5, min_periods=5).mean()
print(data)

w = willr(data['High'], data['Low'], data['Close'], length=14)
print(w)

a = atr(data['High'], data['Low'], data['Close'], length=14)
print(a)

import pandas_ta as ta
a1=ta.atr(data['High'], data['Low'], data['Close'], length=14)
print(a1)

will=mpf.make_addplot(a1,color='blue',panel=1)

mpf.plot(data,type='candle',  style='yahoo',addplot=[will])