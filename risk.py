from typing import Dict, List
from statistics import mean


def var_95(returns: List[float]) -> float:
    ordered = sorted(float(r) for r in returns)
    idx = max(0, int(0.05 * (len(ordered) - 1)))
    return float(ordered[idx])


def beta(returns: List[float], market_returns: List[float]) -> float:
    asset = [float(x) for x in returns]
    market = [float(x) for x in market_returns]
    n = min(len(asset), len(market))
    asset = asset[:n]
    market = market[:n]
    mean_a = mean(asset)
    mean_m = mean(market)
    cov = sum((a - mean_a) * (m - mean_m) for a, m in zip(asset, market)) / max(n - 1, 1)
    var_m = sum((m - mean_m) ** 2 for m in market) / max(n - 1, 1)
    if var_m == 0:
        return 0.0
    return float(cov / var_m)


def sector_exposure(holdings: Dict[str, float], sectors: Dict[str, str]) -> Dict[str, float]:
    totals: Dict[str, float] = {}
    total_value = sum(float(v) for v in holdings.values()) or 1.0
    for symbol, value in holdings.items():
        sector = sectors.get(symbol, "Unknown")
        totals[sector] = totals.get(sector, 0.0) + float(value)
    return {k: round(v / total_value, 4) for k, v in totals.items()}
