import random
from datetime import datetime

class PriceSimulator:
    def __init__(self):
        self.last_prices = {}

    def next_price(self, symbol: str) -> dict:
        base = self.last_prices.get(symbol, random.uniform(50, 250))
        move = random.uniform(-1.5, 1.5)
        price = max(1.0, base + move)
        self.last_prices[symbol] = price
        return {
            "symbol": symbol,
            "price": round(price, 2),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

simulator = PriceSimulator()
