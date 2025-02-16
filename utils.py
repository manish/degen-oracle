import pandas_market_calendars as mcal
from datetime import datetime, timedelta, timezone
import pandas as pd
from models import OptionsEntry

def get_new_price_after_x_hours(entry: OptionsEntry, hours_until_next_trading: float) -> float:
    return entry.last + ((entry.theta / 24) * hours_until_next_trading)

def get_hours_next_trading() -> datetime:
    # Get the current date
    current_date = datetime.now(timezone.utc)

    # Get the NASDAQ trading calendar
    nasdaq = mcal.get_calendar('NASDAQ')

    # Get the next trading day
    next_trading_days = nasdaq.valid_days(start_date=current_date, end_date=current_date + timedelta(days=10))
    next_trading_day = next_trading_days[next_trading_days > pd.Timestamp(current_date)][0]

    # Set the next trading day to 9:30 AM Eastern Time
    next_trading_day = next_trading_day.tz_convert('America/New_York').replace(hour=9, minute=30)

    # Calculate the number of hours between now and the next trading day
    return (next_trading_day - current_date).total_seconds() / 3600