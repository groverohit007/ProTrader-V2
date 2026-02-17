from typing import Dict, List
from statistics import mean, pstdev


def _rsi(prices: List[float], window: int = 14) -> float:
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [d for d in deltas if d > 0]
    losses = [-d for d in deltas if d < 0]
    recent_gains = gains[-window:] if len(gains) >= window else gains
    recent_losses = losses[-window:] if len(losses) >= window else losses
    avg_gain = mean(recent_gains) if recent_gains else 0
    avg_loss = mean(recent_losses) if recent_losses else 1e-8
    rs = avg_gain / (avg_loss + 1e-8)
    return 100 - (100 / (1 + rs))


def explainable_signal(prices: List[float]) -> Dict:
    ret_1 = (prices[-1] / prices[-2]) - 1
    ret_5 = (prices[-1] / prices[-6]) - 1 if len(prices) > 6 else ret_1
    ma_10 = mean(prices[-10:])
    ma_30 = mean(prices[-30:])
    momentum = ret_5
    trend = (ma_10 / ma_30) - 1

    if len(prices) > 21:
        recent_returns = [((prices[i] / prices[i - 1]) - 1) for i in range(len(prices) - 20, len(prices))]
        volatility = pstdev(recent_returns)
    else:
        volatility = 0.01

    rsi = _rsi(prices)
    score = 0.45 * trend + 0.35 * momentum + 0.15 * ret_1 - 0.25 * volatility + 0.05 * ((rsi - 50) / 50)

    buy_p = min(max(0.5 + score, 0.01), 0.98)
    sell_p = min(max(0.5 - score, 0.01), 0.98)
    hold_p = min(max(1 - max(buy_p, sell_p), 0.01), 0.7)
    total = buy_p + sell_p + hold_p
    probs = {"BUY": buy_p / total, "HOLD": hold_p / total, "SELL": sell_p / total}

    signal = max(probs, key=probs.get)
    confidence = probs[signal]
    contributions = {
        "trend_ma10_vs_ma30": round(0.45 * trend, 4),
        "momentum_5d": round(0.35 * momentum, 4),
        "return_1d": round(0.15 * ret_1, 4),
        "volatility_penalty": round(-0.25 * volatility, 4),
        "rsi_bias": round(0.05 * ((rsi - 50) / 50), 4),
    }
    return {
        "signal": signal,
        "confidence": float(round(confidence, 4)),
        "probabilities": {k: float(round(v, 4)) for k, v in probs.items()},
        "contributions": contributions,
    }
