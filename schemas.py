from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field

class PricePoint(BaseModel):
    timestamp: str
    price: float

class PredictionRequest(BaseModel):
    symbol: str
    prices: List[float] = Field(min_length=30)

class PredictionResponse(BaseModel):
    symbol: str
    signal: Literal["BUY", "HOLD", "SELL"]
    confidence: float
    probabilities: Dict[str, float]
    contributions: Dict[str, float]

class StrategyRequest(BaseModel):
    symbol: str
    prices: List[float] = Field(min_length=60)
    short_window: int = 10
    long_window: int = 30
    train_window: int = 40
    test_window: int = 10

class StrategyReport(BaseModel):
    symbol: str
    total_return: float
    sharpe: float
    max_drawdown: float
    walk_forward_splits: int

class OrderRequest(BaseModel):
    user_id: str
    symbol: str
    side: Literal["buy", "sell"]
    qty: float = Field(gt=0)
    mode: Literal["paper", "live"] = "paper"

class Position(BaseModel):
    symbol: str
    qty: float
    avg_price: float

class PortfolioRiskRequest(BaseModel):
    returns: List[float] = Field(min_length=30)
    market_returns: List[float] = Field(min_length=30)
    holdings: Dict[str, float]
    sectors: Dict[str, str]

class NewsItem(BaseModel):
    headline: str
    body: Optional[str] = ""
    source: Optional[str] = "unknown"

class NewsImpactRequest(BaseModel):
    symbol: str
    news: List[NewsItem]

class TeamMember(BaseModel):
    user_id: str
    role: Literal["owner", "analyst", "viewer"]

class TeamCreateRequest(BaseModel):
    org_id: str
    team_name: str
    members: List[TeamMember]

class AlertRequest(BaseModel):
    user_id: str
    symbol: str
    threshold: float
    direction: Literal["above", "below"]
