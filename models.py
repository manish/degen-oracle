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
    max_risk_on__investment: float
    return_over_risk: float

    def __str__(self):
        return (
            f"\n{self.ticker} [{self.short_option.underlying_price:.2f}] {self.expiration} Expiry {self.short_option.dte}DTE {self.side.upper()} Credit Spread:\n"
            f"\t{'Strikes:':<30} -{self.short_option.strike}/+{self.long_option.strike} (-{abs(self.short_option.delta):.2f}/+{abs(self.long_option.delta):.2f})\n"
            f"\t{'Credit Received:':<30} {self.credit_received:.2f}\n"
            f"\t{'Collateral Required:':<30} {self.collateral_required:.2f}\n"
            f"\t{'Maximum Risk:':<30} {self.maximum_risk:.2f}\n"
            f"\t{'Maximum Risk on Investment:':<30} {self.max_risk_on__investment*100:.2f}%\n"
            f"\t{'Return over risk:':<30} {self.return_over_risk*100:.2f}%\n"
        )