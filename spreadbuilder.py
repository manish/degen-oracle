from optionsclient import OptionsClient
from models import Spread
from utils import get_hours_next_trading, get_new_price_after_x_hours
import logging

class SpreadBuilder:
    def __init__(self, client: OptionsClient):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def set_ticker(self, ticker: str):
        self.ticker = ticker
        return self
    
    def set_expiry(self, expiration: str):
        self.expiration = expiration
        return self
    
    def set_side(self, side: str):
        self.side = side
        return self
    
    def set_short_delta(self, delta: float):
        self.short_delta = delta
        return self
    
    def set_long_delta(self, delta: float):
        self.long_delta = delta
        return self

    def run(self):
        recent_expiration, hours_until_next_trading = self._get_expiration_and_hours_until_trading()

        short_option, long_option = self._get_short_long_leg(recent_expiration)

        short_option_new_price, long_option_new_price = self._get_short_long_new_opening_price(
            short_option, long_option, hours_until_next_trading
        )

        credit_received = self._calculate_credit_received(short_option_new_price, long_option_new_price)
        collateral_required = abs((short_option.strike - long_option.strike) * 100)
        maximum_risk = collateral_required - credit_received
        self.logger.debug(f"Credit received: {credit_received}")
        self.logger.debug(f"Collateral required: {collateral_required}")
        self.logger.debug(f"Maximum risk: {maximum_risk}")

        max_risk_on_investment=maximum_risk / collateral_required
        return_over_risk=credit_received / maximum_risk

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
            maximum_risk=maximum_risk,
            max_risk_on_investment=max_risk_on_investment,
            return_over_risk=return_over_risk
        )
    
    def _get_expiration_and_hours_until_trading(self):
        recent_expiration = self.expiration or self.client.get_most_recent_expiration(self.ticker)
        hours_until_next_trading = get_hours_next_trading()
        return recent_expiration, hours_until_next_trading

    def _get_short_long_leg(self, recent_expiration):
        short_option = self.client.get_option_expiration_side_delta(
            self.ticker, recent_expiration, self.side, str(self.short_delta)
        )
        self.logger.debug(f"Short option: {short_option}")
        long_option = self.client.get_option_expiration_side_delta(
            self.ticker, recent_expiration, self.side, str(self.long_delta)
        )
        if short_option.symbol == long_option.symbol:
            new_long_delta = abs(short_option.delta) - 0.01 - abs(self.short_delta - self.long_delta)
            new_long_delta_arg = f"{new_long_delta:.2f}-{abs(short_option.delta) - 0.01:.2f}"
            self.logger.debug(
                f"Long option was same as short option, computing new long option delta: {new_long_delta} "
                f"with arg: {new_long_delta_arg}"
            )
            long_option = self.client.get_option_expiration_side_delta(
                self.ticker, recent_expiration, self.side, new_long_delta
            )
        self.logger.debug(f"Long option: {long_option}")
        return short_option, long_option
    
    def _get_short_long_new_opening_price(self, short_option, long_option, hours_until_next_trading):
        short_option_new_price = get_new_price_after_x_hours(short_option, hours_until_next_trading)
        long_option_new_price = get_new_price_after_x_hours(long_option, hours_until_next_trading)
        self.logger.debug(f"Short option new price: {short_option_new_price}")
        self.logger.debug(f"Long option new price: {long_option_new_price}")
        return short_option_new_price, long_option_new_price
    
    def _calculate_credit_received(self, short_option_new_price, long_option_new_price):
        return (short_option_new_price - long_option_new_price) * 100