from warrenbotfett.api.orders import place_buy_order, place_sell_order
from warrenbotfett.common import Action, BuyOrder, SellOrder, Trading212Ticker


def execute_actions(actions: list[Action]):
    sell_orders: list[SellOrder] = [a for a in actions if isinstance(a, SellOrder)]
    buy_orders: list[BuyOrder] = [a for a in actions if isinstance(a, BuyOrder)]
    for sell_order in sell_orders:
        place_sell_order(
            ticker=sell_order.instrument, quantity=0.0, stop_price=0.0
        )  # TODO
    for buy_order in buy_orders:
        place_buy_order(ticker=buy_order.instrument, quantity=0.0)  # TODO


if __name__ == "__main__":
    actions = [
        SellOrder(
            instrument=Trading212Ticker.AAPL_US_EQ,
            amount=100,
            reasoning="It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued.",
        ),
        BuyOrder(
            instrument=Trading212Ticker.AAPL_US_EQ,
            amount=100,
            reasoning="It's undervalued It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued. It's overvalued.",
        ),
    ]
