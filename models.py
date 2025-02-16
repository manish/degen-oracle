from dataclasses import dataclass


@dataclass
class OptionsEntry:
    symbol:str
    underlying:str
    expiration:str
    side: str
    strike: int
    dte: int
    mid: float
    last: float
    volume: int
    underlying_price: float
    iv: float
    delta: float
    gamma: float
    theta: float


@dataclass
class Spread:
    ticker:str
    side:str
    expiration:str
    short_option: OptionsEntry
    long_option: OptionsEntry
    hours_until_next_trading: float
    short_option_new_price: float
    long_option_new_price: float
    credit_received: float
    collateral_required: float
    maximum_risk: float

    def __str__(self):
        return (
            f"{self.ticker} [{self.short_option.underlying_price}] {self.expiration} {self.short_option.dte}DTE {self.side.upper()} Credit Spread:\n"
            f"\tStrikes: -{self.short_option.strike}/+{self.long_option.strike} (-{abs(self.short_option.delta)}/+{abs(self.long_option.delta)})\n"
            f"\tCredit Received: {self.credit_received}\n"
            f"\tCollateral Required: {self.collateral_required}\n"
            f"\tMaximum Risk: {self.maximum_risk}"
        )