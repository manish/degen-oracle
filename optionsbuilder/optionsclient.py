import requests
from optionsbuilder.models import OptionsEntry

class OptionsClient:
    def __init__(self, token):
        self.token = token

    def get_option_expiration_side_delta(self, ticker, expiration, side: str, delta: str):
        result = self.make_request(f'https://api.marketdata.app/v1/options/chain/{ticker}/?expiration={expiration}&side={side}&delta={delta}')
        for key,value in result.items():
            if isinstance(value, list):
                result[key] = value.pop(0)

        return OptionsEntry(
            symbol=result["optionSymbol"],
            underlying=result["underlying"],
            expiration=result["expiration"],
            side=result["side"],
            strike=result["strike"],
            dte=result["dte"],
            mid=result["mid"],
            last=result["last"],
            volume=result["volume"],
            underlying_price=result["underlyingPrice"],
            iv=result["iv"],
            delta=result["delta"],
            gamma=result["gamma"],
            theta=result["theta"]
        )

    def get_most_recent_expiration(self, ticker):
        return self.get_expirations(ticker)["expirations"].pop(0)

    def get_expirations(self, ticker):
        return self.make_request(f'https://api.marketdata.app/v1/options/expirations/{ticker}')
        
    def make_request(self, url):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code in (200, 203):
            return response.json()
        else:
            raise Exception(f'Failed to retrieve data from {url}: {response.status_code}')