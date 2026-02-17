import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from schemas import AlertRequest
from price_stream import simulator
from store import store

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
