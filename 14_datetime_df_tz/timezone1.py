

import datetime as dt
from zoneinfo import ZoneInfo
new_york_timezone = ZoneInfo('America/New_York')
kolkata_timezone = ZoneInfo('Asia/Kolkata')
utc_timezone=ZoneInfo('UTC')
dt1=dt.datetime.now(tz=utc_timezone)
print(dt1)
dt1=dt.datetime.now(tz=new_york_timezone)
print(dt1)
dt1=dt.datetime.now(tz=kolkata_timezone)
print(dt1)