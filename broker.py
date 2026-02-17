from fastapi import APIRouter, HTTPException

from schemas import OrderRequest
from store import store

router = APIRouter(prefix="/broker", tags=["broker"])


@router.post("/orders")
def place_order(order: OrderRequest):
    symbol = order.symbol.upper()
    if order.mode == "live":
        raise HTTPException(status_code=501, detail="Live trading is not enabled in this demo backend")

    user_positions = store.paper_positions[order.user_id]
    current = user_positions.get(symbol, {"symbol": symbol, "qty": 0.0, "avg_price": 0.0})

    if order.side == "buy":
        new_qty = current["qty"] + order.qty
        current["avg_price"] = current["avg_price"] if current["qty"] else 100.0
        current["qty"] = new_qty
    else:
        if current["qty"] < order.qty:
            raise HTTPException(status_code=400, detail="Not enough quantity to sell")
        current["qty"] -= order.qty

    user_positions[symbol] = current
    return {"status": "filled", "position": current}


@router.get("/positions/{user_id}")
def get_positions(user_id: str):
    return {"user_id": user_id, "positions": list(store.paper_positions[user_id].values())}
