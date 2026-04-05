import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    from datetime import datetime, timezone
    from kitsune.models import Trade, OrderbookSnapshot

    def subscriptions_format(symbols: set[str]) -> list[dict]:
        subs = []
        for s in symbols:
            subs.append({"method": "subscribe", "subscription": {"type": "trades", "coin": s}})
            subs.append({"method": "subscribe", "subscription": {"type": "l2Book", "coin": s, "nSigFigs": None}})
        return subs

    def handle_trades(trades: dict):
        sum = []
        for trade in trades.get("data", []):
            t = Trade(
                exchange="hyperliquid",
                symbol=trade["coin"],
                price=trade["px"],
                side="buy" if trade["side"] == "B" else "sell",
                amount=trade["sz"],
                traded_at=datetime.fromtimestamp(trade["time"] / 1000, tz=timezone.utc)
            )
            sum.append(t)
            print(f"{len(sum)} trades added. Trades: {sum}")

    def handle_orderbook(orders: dict):
        data = orders.get("data", {})
        coin = data.get("coin", "")

        levels = data.get("levels", [[], []])
        bids = [[lv["px"], lv["sz"]] for lv in levels[0]]
        asks = [[lv["px"], lv["sz"]] for lv in levels[1]]
        ob = OrderbookSnapshot(
            exchange="hyperliquid",
            symbol=coin,
            bids=bids,
            asks=asks,
            snapshot_at=datetime.fromtimestamp(data.get("time", 0) / 1000, tz=timezone.utc)
        )
        print(f"Orderbook snapshot added. Orderbook: {ob}")

    def handle_message(msg: dict):
        channel = msg.get("channel")
        if channel == "trades":
            handle_trades(msg)
        elif channel == "l2Book":
            handle_orderbook(msg)

    return handle_message, subscriptions_format


@app.cell
async def _(handle_message, subscriptions_format):
    from kitsune.connection import WSConnection

    WS_URL = "wss://api.hyperliquid.xyz/ws"
    symbols = set(["BTC", "ETH"])

    conn = WSConnection(url=WS_URL)
    async for msg in conn.connect(subscriptions=subscriptions_format(symbols)):
        handle_message(msg)
    return


if __name__ == "__main__":
    app.run()
