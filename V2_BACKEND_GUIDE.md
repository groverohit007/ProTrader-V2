# StockMind-AI v2 Backend

This repository now includes a **mobile-ready FastAPI backend** under \2_backend/\ that extends current app capabilities.

## Included v2 features

1. **Live websocket prices + alerts**
   - \GET /market/quote/{symbol}\
   - \POST /market/alerts\
   - \GET /market/alerts/check/{symbol}\
   - \WS /market/ws/prices/{symbol}\

2. **Explainable AI predictions**
   - \POST /predictions/explain\
   - Returns signal, confidence, probabilities, and per-feature contribution values.

3. **Strategy builder + walk-forward optimization**
   - \POST /strategy/walk-forward\
   - Runs MA-crossover strategy walk-forward splits and reports return/sharpe/max drawdown.

4. **Broker integration (paper/live)**
   - \POST /broker/orders\ (paper supported, live returns 501 placeholder)
   - \GET /broker/positions/{user_id}\

5. **Portfolio risk analytics**
   - \POST /portfolio/risk\
   - Computes VaR(95), beta, sector exposure.

6. **News/sentiment with event impact**
   - \POST /news/impact\
   - Scores sentiment and event-weighted impact per headline.

7. **Multi-user org/team dashboards + audit logs**
   - \POST /org/teams\
   - \GET /org/teams/{org_id}\
   - \POST /org/audit/{org_id}\
   - \GET /org/audit/{org_id}\

## Run locally

\\\ash
uvicorn v2_backend.main:app --reload --port 8000
\\\
