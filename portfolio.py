from fastapi import APIRouter

from schemas import PortfolioRiskRequest
from risk import beta, sector_exposure, var_95

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.post("/risk")
def portfolio_risk(req: PortfolioRiskRequest):
    return {
        "var_95": var_95(req.returns),
        "beta": beta(req.returns, req.market_returns),
        "sector_exposure": sector_exposure(req.holdings, req.sectors),
    }
