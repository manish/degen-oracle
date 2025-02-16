from optionsclient import OptionsClient
from models import Spread
from utils import get_hours_next_trading, get_new_price_after_x_hours

class SpreadBuilder:
    def __init__(self, client:OptionsClient):
        self.client = client

    def set_ticker(self, ticker:str):
        self.ticker = ticker
        return self
    
    def set_side(self, side:str):
        self.side = side
        return self
    
    def set_short_delta(self, delta:float):
        self.short_delta = delta
        return self
    
    def set_long_delta(self, delta:float):
        self.long_delta = delta
        return self
    
    def run(self):
        recent_expiration = self.client.get_most_recent_expiration(self.ticker)
        short_option = self.client.get_option_expiration_side_delta(self.ticker, recent_expiration, self.side, self.short_delta)
        long_option = self.client.get_option_expiration_side_delta(self.ticker, recent_expiration, self.side, self.long_delta)

        hours_until_next_trading = get_hours_next_trading()

        # Calculate the new price for short_option when the trading opens
        short_option_new_price = get_new_price_after_x_hours(short_option, hours_until_next_trading)
        long_option_new_price = get_new_price_after_x_hours(long_option, hours_until_next_trading)
        credit_received = (short_option_new_price-long_option_new_price)*100
        collateral_required = abs((short_option.strike-long_option.strike)*100)
        maximum_risk=collateral_required - credit_received

        return Spread(
            ticker=self.ticker,
            side=self.side,
            expiration=recent_expiration,
            short_option=short_option,
            long_option=long_option,
            hours_until_next_trading=hours_until_next_trading,
            short_option_new_price=short_option_new_price,
            long_option_new_price=long_option_new_price,
            credit_received=credit_received,
            collateral_required=collateral_required,
            maximum_risk=maximum_risk
        )