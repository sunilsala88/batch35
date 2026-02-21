#sma,ema,macd,rsi,adx,bollinger,supertrend,atr

#talib
#pandasta
#ta

from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
import yfinance as yf
import mplfinance as mpf


def _ma(close: pd.Series, length: int, mamode: str) -> pd.Series:
	mode = (mamode or "sma").lower()
	if mode == "ema":
		return close.ewm(span=length, adjust=False, min_periods=length).mean()
	return close.rolling(window=length, min_periods=length).mean()


def _non_zero_range(upper: pd.Series, lower: pd.Series) -> pd.Series:
	result = (upper - lower).astype(float)
	return result.mask(result == 0, np.finfo(float).eps)


def bbands(
	close: pd.Series,
	length: Optional[int] = None,
	lower_std: Optional[float] = None,
	upper_std: Optional[float] = None,
	ddof: Optional[int] = None,
	mamode: Optional[str] = None,
	talib: Optional[bool] = None,
	offset: Optional[int] = None,
	**kwargs: Dict[str, Any],
) -> pd.DataFrame:
	"""Bollinger Bands (standalone, no pandas_ta dependency)."""
	length = int(length) if isinstance(length, int) and length > 0 else 5
	if close is None:
		return pd.DataFrame()

	if not isinstance(close, pd.Series):
		close = pd.Series(close)

	lower_std = float(lower_std) if lower_std is not None and lower_std > 0 else 2.0
	upper_std = float(upper_std) if upper_std is not None and upper_std > 0 else 2.0
	ddof = int(ddof) if isinstance(ddof, int) and 0 <= ddof < length else 1
	mamode = mamode or "sma"
	_ = talib
	offset = int(offset) if isinstance(offset, int) else 0

	std_dev = close.rolling(window=length, min_periods=length).std(ddof=ddof)
	lower_deviations = lower_std * std_dev
	upper_deviations = upper_std * std_dev

	mid = _ma(close, length=length, mamode=mamode)
	lower = mid - lower_deviations
	upper = mid + upper_deviations

	ulr = _non_zero_range(upper, lower)
	bandwidth = 100 * ulr / mid
	percent = _non_zero_range(close, lower) / ulr

	if offset != 0:
		lower = lower.shift(offset)
		mid = mid.shift(offset)
		upper = upper.shift(offset)
		bandwidth = bandwidth.shift(offset)
		percent = percent.shift(offset)

	if "fillna" in kwargs:
		fill_value = kwargs["fillna"]
		lower.fillna(fill_value, inplace=True)
		mid.fillna(fill_value, inplace=True)
		upper.fillna(fill_value, inplace=True)
		bandwidth.fillna(fill_value, inplace=True)
		percent.fillna(fill_value, inplace=True)

	_props = f"_{length}_{lower_std}_{upper_std}"
	lower.name = f"BBL{_props}"
	mid.name = f"BBM{_props}"
	upper.name = f"BBU{_props}"
	bandwidth.name = f"BBB{_props}"
	percent.name = f"BBP{_props}"

	lower.attrs["category"] = "volatility"
	mid.attrs["category"] = "volatility"
	upper.attrs["category"] = "volatility"
	bandwidth.attrs["category"] = "volatility"
	percent.attrs["category"] = "volatility"

	data = {
		lower.name: lower,
		mid.name: mid,
		upper.name: upper,
		bandwidth.name: bandwidth,
		percent.name: percent,
	}
	df = pd.DataFrame(data, index=close.index)
	df.attrs["name"] = f"BBANDS{_props}"
	df.attrs["category"] = "volatility"

	return df

data=yf.download('TSLA',period='max',multi_level_index=False)
print(data)

#sma
a=data['Close'].rolling(window=5, min_periods=5).mean()
print(a)

#ema
data['ema']=data['Close'].ewm(span=15, adjust=False, min_periods=15).mean()

b=bbands(data['Close'],length=12)
print(b)

import pandas_ta as ta
c=ta.bbands(data['Close'],length=12)
print(c)

