from consts import API_KEY
from optionsclient import OptionsClient
from spreadbuilder import SpreadBuilder
import argparse

def validate_side(value):
    if value not in ["call", "put"]:
        raise argparse.ArgumentTypeError(f"Invalid side value: {value}. Allowed values are 'call' or 'put'.")
    return value

def validate_delta(value):
    try:
        fvalue = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid delta value: {value}. Must be a float.")
    if not (0 <= fvalue <= 1):
        raise argparse.ArgumentTypeError(f"Invalid delta value: {value}. Must be between 0 and 1.")
    return fvalue

parser = argparse.ArgumentParser(description="Options ilder")
subparsers = parser.add_subparsers(dest="command")

credit_spread_parser = subparsers.add_parser("credit-spread", help="Build a credit spread")
credit_spread_parser.add_argument("ticker", type=str, help="Ticker symbol")
credit_spread_parser.add_argument("side", type=validate_side, help="Side of the option (call or put)")
credit_spread_parser.add_argument("short_delta", type=validate_delta, nargs="?", default=0.25, help="Short delta (default: 0.25)")
credit_spread_parser.add_argument("long_delta", type=validate_delta, nargs="?", default=0.20, help="Long delta (default: 0.20)")
credit_spread_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

args = parser.parse_args()

if args.command == "credit-spread":
    ticker = args.ticker
    side = args.side
    short_delta = args.short_delta
    long_delta = args.long_delta
    debug = args.debug

    client = OptionsClient(API_KEY)
    spread = (SpreadBuilder(client)
              .set_debug_mode(debug)
              .set_ticker(ticker)
              .set_side(side)
              .set_short_delta(short_delta)
              .set_long_delta(long_delta)
              .run())
    print(spread)