

import pendulum as dt
import logging
import time

# timezone to use for logging timestamps
time_zone = 'UTC'
tickers = ['ETH','AAVE','BCH','LTC']

class PendulumFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = dt.from_timestamp(record.created, tz=time_zone)
        if datefmt:
            return ct.strftime(datefmt)
        return ct.format('YYYY-MM-DD HH:mm:ss ZZ')


log_filename = f'strategy_{dt.now(time_zone).to_date_string()}.log'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()

handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
handler.setLevel(logging.INFO)
handler.setFormatter(PendulumFormatter("%(asctime)s - %(message)s"))
logger.addHandler(handler)

logger.info(f"Current time: {dt.now(time_zone)} - Strategy started")


def main_strategy_code():
    print("inside main strategy")
    logger.info(f"inside main strategy {tickers}")


while True:
    ct = dt.now(time_zone)
    print(ct)
    # run every 5 min
    # if ct.second==1 and ct.minute%5==0:
    if ct.second == 1:
        print('new candle started')

        main_strategy_code()
    time.sleep(1)