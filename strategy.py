from fastapi import APIRouter
from v2_backend.schemas import StrategyRequest, StrategyReport
from v2_backend.services.strategy import walk_forward_report

router = APIRouter(prefix="/strategy", tags=["strategy"])

@router.post("/walk-forward", response_model=StrategyReport)
def run_walk_forward(req: StrategyRequest):
    report = walk_forward_report(
        req.prices, req.short_window, req.long_window, req.train_window, req.test_window
    )
    return StrategyReport(symbol=req.symbol.upper(), **report)
