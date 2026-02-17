from fastapi import APIRouter
from math import sqrt
from statistics import mean, pstdev

from schemas import StrategyRequest, StrategyReport

router = APIRouter(prefix="/strategy", tags=["strategy"])


def walk_forward_report(prices, short_window, long_window, train_window, test_window):
    splits = 0
    strategy_returns = []
    for start in range(train_window, len(prices) - test_window, test_window):
        test = prices[start : start + test_window]
        if len(test) < test_window or start < long_window:
            continue
        ma_short = mean(prices[start - short_window : start])
        ma_long = mean(prices[start - long_window : start])
        direction = 1 if ma_short > ma_long else -1
        ret = direction * ((test[-1] / test[0]) - 1)
        strategy_returns.append(ret)
        splits += 1

    total = 1.0
    for r in strategy_returns:
        total *= 1 + r
    total_return = total - 1 if strategy_returns else 0.0
    sharpe = (mean(strategy_returns) / (pstdev(strategy_returns) + 1e-8)) * sqrt(252) if strategy_returns else 0.0

    cumulative = []
    run = 1.0
    for r in strategy_returns:
        run *= 1 + r
        cumulative.append(run)
    peak = 1.0
    max_drawdown = 0.0
    for c in cumulative:
        peak = max(peak, c)
        dd = (c / peak) - 1
        max_drawdown = min(max_drawdown, dd)

    return {
        "total_return": round(float(total_return), 4),
        "sharpe": round(float(sharpe), 4),
        "max_drawdown": round(float(max_drawdown), 4),
        "walk_forward_splits": splits,
    }


@router.post("/walk-forward", response_model=StrategyReport)
def run_walk_forward(req: StrategyRequest):
    report = walk_forward_report(
        req.prices, req.short_window, req.long_window, req.train_window, req.test_window
    )
    return StrategyReport(symbol=req.symbol.upper(), **report)
