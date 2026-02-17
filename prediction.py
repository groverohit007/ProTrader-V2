from typing import Dict, List
import numpy as np

def _rsi(prices: List[float], window: int = 14) -> float:
    arr = np.array(prices, dtype=float)
    deltas = np.diff(arr)
    gains = np.clip(deltas, 0, None)
    losses = -np.clip(deltas, None, 0)
    avg_gain = gains[-window:].mean() if len(gains) >= window else gains.mean() if len(gains) else 0
    avg_loss = losses[-window:].mean() if len(losses) >= window else losses.mean() if len(losses) else 1e-8
    rs = avg_gain / (avg_loss + 1e-8)
    return 100 - (100 / (1 + rs))

def explainable_signal(prices: List[float]) -> Dict:
    arr = np.array(prices, dtype=float)
    ret_1 = (arr[-1] / arr[-2]) - 1
    ret_5 = (arr[-1] / arr[-6]) - 1 if len(arr) > 6 else ret_1
    ma_10 = arr[-10:].mean()
    ma_30 = arr[-30:].mean()
    momentum = ret_5
    trend = (ma_10 / ma_30) - 1
    volatility = np.std(np.diff(arr[-20:]) / arr[-21:-1]) if len(arr) > 21 else 0.01
    rsi = _rsi(prices)

    score = 0.45 * trend + 0.35 * momentum + 0.15 * (ret_1) - 0.25 * volatility + 0.05 * ((rsi - 50) / 50)

    buy_p = float(np.clip(0.5 + score, 0.01, 0.98))
    sell_p = float(np.clip(0.5 - score, 0.01, 0.98))
    hold_p = float(np.clip(1 - max(buy_p, sell_p), 0.01, 0.7))
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
