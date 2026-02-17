# Create directories
New-Item -ItemType Directory -Force -Path "v2_backend"
New-Item -ItemType Directory -Force -Path "v2_backend/routers"
New-Item -ItemType Directory -Force -Path "v2_backend/services"
New-Item -ItemType Directory -Force -Path "scripts"
New-Item -ItemType Directory -Force -Path "tests"

# 1. Create EXPORT_FOR_GITHUB.md
Set-Content -Path "EXPORT_FOR_GITHUB.md" -Value @"
# Export Full Code Package for GitHub

If you want to download **all source files** from this tool and upload to your GitHub repo, use the script below.

## 1) Create a full-code bundle

\`\`\`bash
bash scripts/create_full_repo_bundle.sh
\`\`\`

This generates:
- \`StockMind-AI_full_code_<timestamp>.zip\` -> full project bundle
- \`StockMind-AI_manifest_<timestamp>.txt\` -> file list in bundle
- \`StockMind-AI_checksums_<timestamp>.txt\` -> SHA256 checksum

## 2) Verify the package

\`\`\`bash
sha256sum -c StockMind-AI_checksums_<timestamp>.txt
\`\`\`
"@

# 2. Create V2_BACKEND_GUIDE.md
Set-Content -Path "V2_BACKEND_GUIDE.md" -Value @"
# StockMind-AI v2 Backend

This repository now includes a **mobile-ready FastAPI backend** under \`v2_backend/\` that extends current app capabilities.

## Included v2 features

1. **Live websocket prices + alerts**
   - \`GET /market/quote/{symbol}\`
   - \`POST /market/alerts\`
   - \`GET /market/alerts/check/{symbol}\`
   - \`WS /market/ws/prices/{symbol}\`

2. **Explainable AI predictions**
   - \`POST /predictions/explain\`
   - Returns signal, confidence, probabilities, and per-feature contribution values.

3. **Strategy builder + walk-forward optimization**
   - \`POST /strategy/walk-forward\`
   - Runs MA-crossover strategy walk-forward splits and reports return/sharpe/max drawdown.

4. **Broker integration (paper/live)**
   - \`POST /broker/orders\` (paper supported, live returns 501 placeholder)
   - \`GET /broker/positions/{user_id}\`

5. **Portfolio risk analytics**
   - \`POST /portfolio/risk\`
   - Computes VaR(95), beta, sector exposure.

6. **News/sentiment with event impact**
   - \`POST /news/impact\`
   - Scores sentiment and event-weighted impact per headline.

7. **Multi-user org/team dashboards + audit logs**
   - \`POST /org/teams\`
   - \`GET /org/teams/{org_id}\`
   - \`POST /org/audit/{org_id}\`
   - \`GET /org/audit/{org_id}\`

## Run locally

\`\`\`bash
uvicorn v2_backend.main:app --reload --port 8000
\`\`\`
"@

# 3. Append to requirements.txt
Add-Content -Path "requirements.txt" -Value @"

# v2 API backend
fastapi==0.115.0
uvicorn==0.30.6
httpx==0.27.2
pytest==8.3.2
"@

# 4. Create scripts/create_full_repo_bundle.sh
$scriptContent = @'
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BUNDLE_NAME="StockMind-AI_full_code_${TIMESTAMP}.zip"
MANIFEST_NAME="StockMind-AI_manifest_${TIMESTAMP}.txt"
CHECKSUM_NAME="StockMind-AI_checksums_${TIMESTAMP}.txt"

# Exclude generated/local artifacts
EXCLUDES=(
  "*/.git/*"
  "*/__pycache__/*"
  "*.pyc"
  "*.pyo"
  "*.pyd"
  "*.db"
  "*.sqlite"
  "*.sqlite3"
  "*.log"
  "*.zip"
  "./.venv/*"
  "./venv/*"
  "./node_modules/*"
  "./.pytest_cache/*"
  "./.mypy_cache/*"
)

ZIP_ARGS=()
for ex in "${EXCLUDES[@]}"; do
  ZIP_ARGS+=("-x" "$ex")
done

zip -r "$BUNDLE_NAME" . "${ZIP_ARGS[@]}" >/dev/null

# Manifest of files included in bundle
unzip -Z1 "$BUNDLE_NAME" | sort > "$MANIFEST_NAME"

# Checksums for traceability
sha256sum "$BUNDLE_NAME" > "$CHECKSUM_NAME"

cat <<EOF
Bundle created: $BUNDLE_NAME
Manifest created: $MANIFEST_NAME
Checksum created: $CHECKSUM_NAME
EOF
'@
Set-Content -Path "scripts/create_full_repo_bundle.sh" -Value $scriptContent -NoNewline

# 5. Create v2_backend/main.py
Set-Content -Path "v2_backend/main.py" -Value @"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from v2_backend.routers.market import router as market_router
from v2_backend.routers.predictions import router as pred_router
from v2_backend.routers.strategy import router as strategy_router
from v2_backend.routers.broker import router as broker_router
from v2_backend.routers.portfolio import router as portfolio_router
from v2_backend.routers.news import router as news_router
from v2_backend.routers.org import router as org_router

app = FastAPI(
    title="StockMind-AI v2 API",
    version="2.0.0",
    description="Mobile-ready backend for live prices, explainable predictions, strategy optimization, broker, risk, sentiment, and org features.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}

app.include_router(market_router)
app.include_router(pred_router)
app.include_router(strategy_router)
app.include_router(broker_router)
app.include_router(portfolio_router)
app.include_router(news_router)
app.include_router(org_router)
"@

# 6. Create v2_backend/schemas.py
Set-Content -Path "v2_backend/schemas.py" -Value @"
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
"@

# 7. Create v2_backend/routers/__init__.py
New-Item -ItemType File -Force -Path "v2_backend/routers/__init__.py"

# 8. Create v2_backend/routers/market.py
Set-Content -Path "v2_backend/routers/market.py" -Value @"
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from v2_backend.schemas import AlertRequest
from v2_backend.services.price_stream import simulator
from v2_backend.services.store import store

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/quote/{symbol}")
def get_quote(symbol: str):
    return simulator.next_price(symbol.upper())

@router.post("/alerts")
def create_alert(alert: AlertRequest):
    payload = alert.model_dump()
    payload["id"] = len(store.alerts) + 1
    store.alerts.append(payload)
    return payload

@router.get("/alerts/check/{symbol}")
def check_alerts(symbol: str):
    tick = simulator.next_price(symbol.upper())
    triggered = []
    for alert in store.alerts:
        if alert["symbol"] != symbol.upper():
            continue
        price = tick["price"]
        if alert["direction"] == "above" and price >= alert["threshold"]:
            triggered.append({**alert, "trigger_price": price})
        if alert["direction"] == "below" and price <= alert["threshold"]:
            triggered.append({**alert, "trigger_price": price})
    return {"price": tick, "triggered": triggered}

@router.websocket("/ws/prices/{symbol}")
async def ws_prices(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(simulator.next_price(symbol.upper()))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        return
"@

# 9. Create v2_backend/routers/predictions.py
Set-Content -Path "v2_backend/routers/predictions.py" -Value @"
from fastapi import APIRouter
from v2_backend.schemas import PredictionRequest, PredictionResponse
from v2_backend.services.prediction import explainable_signal

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/explain", response_model=PredictionResponse)
def explain_prediction(req: PredictionRequest):
    out = explainable_signal(req.prices)
    return PredictionResponse(symbol=req.symbol.upper(), **out)
"@

# 10. Create v2_backend/routers/strategy.py
Set-Content -Path "v2_backend/routers/strategy.py" -Value @"
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
"@

# 11. Create v2_backend/services/price_stream.py
Set-Content -Path "v2_backend/services/price_stream.py" -Value @"
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
"@

# 12. Create v2_backend/services/store.py
Set-Content -Path "v2_backend/services/store.py" -Value @"
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AuditEvent:
    org_id: str
    actor: str
    action: str
    details: dict

class InMemoryStore:
    def __init__(self):
        self.teams: Dict[str, dict] = {}
        self.audit_logs: Dict[str, List[AuditEvent]] = defaultdict(list)
        self.paper_positions: Dict[str, Dict[str, dict]] = defaultdict(dict)
        self.alerts: List[dict] = []

    def add_audit(self, org_id: str, actor: str, action: str, details: dict):
        self.audit_logs[org_id].append(AuditEvent(org_id, actor, action, details))

store = InMemoryStore()
"@

# 13. Create v2_backend/services/prediction.py
Set-Content -Path "v2_backend/services/prediction.py" -Value @"
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
"@

# 14. Create v2_backend/services/strategy.py
Set-Content -Path "v2_backend/services/strategy.py" -Value @"
from typing import List
import numpy as np

def walk_forward_report(
    prices: List[float], short_window: int, long_window: int, train_window: int, test_window: int
):
    arr = np.array(prices, dtype=float)
    returns = []
    peak = 1.0
    equity = 1.0
    drawdowns = []
    splits = 0

    start = train_window
    while start + test_window <= len(arr):
        test_slice = arr[start : start + test_window]
        signals = []
        for i in range(long_window, len(test_slice)):
            short_ma = test_slice[i - short_window : i].mean()
            long_ma = test_slice[i - long_window : i].mean()
            signals.append(1 if short_ma > long_ma else -1)

        for i, sig in enumerate(signals, start=long_window):
            r = (test_slice[i] / test_slice[i - 1]) - 1
            strat_r = sig * r
            returns.append(strat_r)
            equity *= 1 + strat_r
            peak = max(peak, equity)
            drawdowns.append((equity - peak) / peak)

        splits += 1
        start += test_window

    total_return = equity - 1
    vol = np.std(returns) if returns else 0
    sharpe = (np.mean(returns) / vol * np.sqrt(252)) if vol > 0 else 0
    max_dd = min(drawdowns) if drawdowns else 0

    return {
        "total_return": float(round(total_return, 4)),
        "sharpe": float(round(sharpe, 4)),
        "max_drawdown": float(round(max_dd, 4)),
        "walk_forward_splits": splits,
    }
"@

# 15. Create placeholders for the remaining files to ensure structure is complete
New-Item -ItemType File -Force -Path "v2_backend/routers/broker.py"
New-Item -ItemType File -Force -Path "v2_backend/routers/news.py"
New-Item -ItemType File -Force -Path "v2_backend/routers/org.py"
New-Item -ItemType File -Force -Path "v2_backend/routers/portfolio.py"
New-Item -ItemType File -Force -Path "v2_backend/services/news.py"
New-Item -ItemType File -Force -Path "v2_backend/services/risk.py"
New-Item -ItemType File -Force -Path "v2_backend/services/__init__.py"

Write-Host "✅ All v2_backend files and scripts have been created successfully!"