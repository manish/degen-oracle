from consts import API_KEY
from optionsclient import OptionsClient
from spreadbuilder import SpreadBuilder

ticker = "HIMS"
client = OptionsClient(API_KEY)

print(SpreadBuilder(client).set_ticker(ticker).set_side("call").set_short_delta(0.25).set_long_delta(0.20).run())

print(SpreadBuilder(client).set_ticker(ticker).set_side("put").set_short_delta(0.25).set_long_delta(0.20).run())