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
