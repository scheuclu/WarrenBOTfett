import yfinance as yf

from warrenbotfett.api.account import cash
from warrenbotfett.api.yf import get_instrument_price
from warrenbotfett.common import YFinanceTicker
from warrenbotfett.db.write import store_sp500_performance_analysis
from warrenbotfett.models import Cash

eur_usd = yf.Ticker("EURUSD=X").fast_info.last_price
assert isinstance(eur_usd, float)

account_cash = cash()
assert isinstance(account_cash, Cash)
assert hasattr(account_cash, "total")
assert isinstance(account_cash.total, float)

account_total_usd = round(account_cash.total * eur_usd, 2)
print(f"{account_total_usd=}")
sp500_price_usd = get_instrument_price(YFinanceTicker.SPY)
print(f"{sp500_price_usd=}")
success = store_sp500_performance_analysis(
    spy_usd=sp500_price_usd, portfolio_value_usd=account_total_usd
)
assert success, "Writing to database failed"
