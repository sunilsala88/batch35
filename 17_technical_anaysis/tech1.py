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


def _ema(close: pd.Series, length: int) -> pd.Series:
	return close.ewm(span=length, adjust=False, min_periods=length).mean()


def _cross(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
	return (series_a > series_b) & (series_a.shift(1) <= series_b.shift(1))


def signals(
	indicator: pd.Series,
	xa: Optional[float] = 0,
	xb: Optional[float] = None,
	xseries: Optional[pd.Series] = None,
	xseries_a: Optional[pd.Series] = None,
	xseries_b: Optional[pd.Series] = None,
	cross_values: bool = True,
	cross_series: bool = True,
	offset: int = 0,
) -> pd.DataFrame:
	name = indicator.name or "indicator"
	out: Dict[str, pd.Series] = {}

	if cross_values:
		if xa is not None:
			xa_series = pd.Series(float(xa), index=indicator.index)
			out[f"{name}_XA_UP"] = _cross(indicator, xa_series).astype(int)
			out[f"{name}_XA_DN"] = _cross(xa_series, indicator).astype(int)
		if xb is not None:
			xb_series = pd.Series(float(xb), index=indicator.index)
			out[f"{name}_XB_UP"] = _cross(indicator, xb_series).astype(int)
			out[f"{name}_XB_DN"] = _cross(xb_series, indicator).astype(int)

	if cross_series:
		ref_main = xseries if xseries is not None else pd.Series(0.0, index=indicator.index)
		ref_a = xseries_a if xseries_a is not None else ref_main
		ref_b = xseries_b if xseries_b is not None else ref_main
		out[f"{name}_XS_A_UP"] = _cross(indicator, ref_a).astype(int)
		out[f"{name}_XS_A_DN"] = _cross(ref_a, indicator).astype(int)
		out[f"{name}_XS_B_UP"] = _cross(indicator, ref_b).astype(int)
		out[f"{name}_XS_B_DN"] = _cross(ref_b, indicator).astype(int)

	df = pd.DataFrame(out, index=indicator.index)
	if offset:
		df = df.shift(offset)
	return df


def macd(
	close: pd.Series,
	fast: Optional[int] = None,
	slow: Optional[int] = None,
	signal: Optional[int] = None,
	talib: Optional[bool] = None,
	offset: Optional[int] = None,
	**kwargs: Dict[str, Any],
) -> pd.DataFrame:
	"""Compute MACD using only pandas operations.

	Inputs:
		close: Price series (typically close prices).
		fast: Fast EMA period. Default is 12.
		slow: Slow EMA period. Default is 26.
		signal: Signal EMA period applied on MACD line. Default is 9.
		talib: Kept for API compatibility; not used in this standalone version.
		offset: Shift output columns by this many periods.
		kwargs:
			asmode (bool): If True, uses AS mode (MACD := MACD - signal).
			fillna (Any): Fill NaN values in MACD, histogram, and signal columns.
			signal_indicators (bool): If True, append crossover signal columns.

	Output:
		A DataFrame indexed like ``close`` with 3 base columns:
		- ``MACD_{fast}_{slow}_{signal}`` (or ``MACDAS_...`` in AS mode)
		- ``MACDh_{fast}_{slow}_{signal}`` (histogram)
		- ``MACDs_{fast}_{slow}_{signal}`` (signal line)
		If ``signal_indicators=True``, extra binary crossover columns are concatenated.
	"""
	fast = int(fast) if isinstance(fast, int) and fast > 0 else 12
	slow = int(slow) if isinstance(slow, int) and slow > 0 else 26
	signal = int(signal) if isinstance(signal, int) and signal > 0 else 9
	if slow < fast:
		fast, slow = slow, fast

	length = slow + signal - 1
	if close is None:
		return pd.DataFrame()
	if not isinstance(close, pd.Series):
		close = pd.Series(close)
	if close.size < length:
		return pd.DataFrame(index=close.index)

	_ = talib
	offset = int(offset) if isinstance(offset, int) else 0
	as_mode = bool(kwargs.setdefault("asmode", False))

	fastma = _ema(close, length=fast)
	slowma = _ema(close, length=slow)

	macd_line = fastma - slowma
	first_valid = macd_line.first_valid_index()
	if first_valid is not None:
		macd_fvi = macd_line.loc[first_valid:]
		signalma = _ema(macd_fvi, length=signal).reindex(close.index)
	else:
		signalma = pd.Series(np.nan, index=close.index)
	histogram = macd_line - signalma

	if as_mode:
		macd_line = macd_line - signalma
		first_valid = macd_line.first_valid_index()
		if first_valid is not None:
			macd_fvi = macd_line.loc[first_valid:]
			signalma = _ema(macd_fvi, length=signal).reindex(close.index)
		else:
			signalma = pd.Series(np.nan, index=close.index)
		histogram = macd_line - signalma

	if offset != 0:
		macd_line = macd_line.shift(offset)
		histogram = histogram.shift(offset)
		signalma = signalma.shift(offset)

	if "fillna" in kwargs:
		fill_value = kwargs["fillna"]
		macd_line = macd_line.fillna(fill_value)
		histogram = histogram.fillna(fill_value)
		signalma = signalma.fillna(fill_value)

	asmode_text = "AS" if as_mode else ""
	props = f"_{fast}_{slow}_{signal}"
	macd_line.name = f"MACD{asmode_text}{props}"
	histogram.name = f"MACD{asmode_text}h{props}"
	signalma.name = f"MACD{asmode_text}s{props}"

	macd_line.attrs["category"] = "momentum"
	histogram.attrs["category"] = "momentum"
	signalma.attrs["category"] = "momentum"

	df = pd.DataFrame(
		{
			macd_line.name: macd_line,
			histogram.name: histogram,
			signalma.name: signalma,
		},
		index=close.index,
	)
	df.attrs["name"] = f"MACD{asmode_text}{props}"
	df.attrs["category"] = "momentum"

	signal_indicators = bool(kwargs.pop("signal_indicators", False))
	if not signal_indicators:
		return df

	signalsdf = pd.concat(
		[
			df,
			signals(
				indicator=histogram,
				xa=kwargs.pop("xa", 0),
				xb=kwargs.pop("xb", None),
				xseries=kwargs.pop("xseries", None),
				xseries_a=kwargs.pop("xseries_a", None),
				xseries_b=kwargs.pop("xseries_b", None),
				cross_values=kwargs.pop("cross_values", True),
				cross_series=kwargs.pop("cross_series", True),
				offset=offset,
			),
			signals(
				indicator=macd_line,
				xa=kwargs.pop("xa", 0),
				xb=kwargs.pop("xb", None),
				xseries=kwargs.pop("xseries", None),
				xseries_a=kwargs.pop("xseries_a", None),
				xseries_b=kwargs.pop("xseries_b", None),
				cross_values=kwargs.pop("cross_values", False),
				cross_series=kwargs.pop("cross_series", True),
				offset=offset,
			),
		],
		axis=1,
	)

	return signalsdf


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
	"""Compute Bollinger Bands using only pandas operations.

	Inputs:
		close: Price series (typically close prices).
		length: Moving window length. Default is 5.
		lower_std: Lower band standard deviation multiplier. Default is 2.0.
		upper_std: Upper band standard deviation multiplier. Default is 2.0.
		ddof: Delta degrees of freedom for rolling std. Default is 1.
		mamode: Basis moving average mode: ``"sma"`` or ``"ema"``.
		talib: Kept for API compatibility; not used in this standalone version.
		offset: Shift output columns by this many periods.
		kwargs:
			fillna (Any): Fill NaN values in all output columns.

	Output:
		A DataFrame indexed like ``close`` with 5 columns:
		- ``BBL_{length}_{lower_std}_{upper_std}``: lower band
		- ``BBM_{length}_{lower_std}_{upper_std}``: middle band
		- ``BBU_{length}_{lower_std}_{upper_std}``: upper band
		- ``BBB_{length}_{lower_std}_{upper_std}``: bandwidth (%)
		- ``BBP_{length}_{lower_std}_{upper_std}``: percent position in band range
	"""
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

data=yf.download('TSLA',period='5y',multi_level_index=False)
print(data)

#sma
data['sma']=data['Close'].rolling(window=5, min_periods=5).mean()


#ema
data['ema']=data['Close'].ewm(span=15, adjust=False, min_periods=15).mean()

b=bbands(data['Close'],length=12)
print(b)

m=macd(data['Close'])
print(m)



# s1=mpf.make_addplot(data['sma'],color='blue')
# s2=mpf.make_addplot(data['ema'],color='red')
# mpf.plot(data,type='candle',style='yahoo',addplot=[s1,s2])



# lower=mpf.make_addplot(b['BBL_12_2.0_2.0'],color='blue')
# middle=mpf.make_addplot(b['BBM_12_2.0_2.0'],color='red')
# upper=mpf.make_addplot(b['BBU_12_2.0_2.0'],color='green')
# mpf.plot(data,type='candle',style='yahoo',addplot=[lower,middle,upper])


macd=mpf.make_addplot(m['MACD_12_26_9'],color='blue',panel=1)
signal=mpf.make_addplot(m['MACDs_12_26_9'],color='red',panel=1)
histogram=mpf.make_addplot(m['MACDh_12_26_9'],color='green',type='bar',panel=1)
mpf.plot(data,type='candle',  style='yahoo',addplot=[macd,signal,histogram])